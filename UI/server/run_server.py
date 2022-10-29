from dotenv import load_dotenv
import asyncio
from pathlib import Path
import websockets
import time
import sys
import json
import os

import serial
import threading
import queue


from notes_to_learn import (
    phase_1_notes, phase_2_notes, phase_3_notes
)

load_dotenv()

ENV_NAME = os.environ.get('ENV_NAME')
WEBSOCKET_IP = os.environ.get('WEBSOCKET_IP', 'localhost')
PORT = os.environ.get('PORT', 8765)

LOG_DIR = os.environ.get('LOG_DIR', './')


if ENV_NAME == 'PC_TEST':
    from dummy_controller import (
        ServoController, NOTE_TO_SERVO_MAP
    )
else:
    PROJECT_ROOT = os.path.dirname(os.path.dirname((os.path.dirname(__file__))))
    sys.path.append(PROJECT_ROOT)
    from controller import (
        ServoController, NOTE_TO_SERVO_MAP
    )


class FluteListener:
    '''
    Listens to Bt signals from flute
    '''
    def __init__(self):
        try:
            self.btSerial = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=0.5)
            self.btSerial.write(b"Hi")
        except:
            print('Error reading btSerial')

        self.positions = [0, 0, 0, 0, 0, 0]

    def _listener(self, q):
        print('-- starting bt listener --')
        self.btSerial.write(b"Hi")
        while True:
            data = self.btSerial.readline()
            if not data:
                time.sleep(0.1)
                continue
            print('got data')
            q.put(data)

    def _processor(self, q):
        while True:
            servo_ind = None
            bt_command = q.get()
            print(bt_command)
            bt_command = bt_command.decode("utf-8")
            for char in bt_command:
                if char == '^' and isinstance(servo_ind, int):
                    self.positions[servo_ind] = 0
                elif char == '_' and isinstance(servo_ind, int):
                    self.positions[servo_ind] = 1
                else:
                    try:
                        servo_ind = int(char)
                    except Exception as e:
                        print(f'Cannot cast to int: {char}')

    def start(self):
        if ENV_NAME == 'PC_TEST':
            return
        q = queue.Queue()
        threading.Thread(
            target=self._listener,
            args=(q, )
        ).start()
        threading.Thread(
            target=self._processor,
            args=(q, )
        ).start()

    def stop(self):
        pass

    def get_current_positions(self):
        if ENV_NAME == 'PC_TEST':
            import random
            ans = [
                random.randint(0, 1), random.randint(0, 1), random.randint(0, 1),
                random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)
            ]
            return ans
        return [x for x in self.positions]


class Logger:
    pass


class MainServer:
    '''
    Assumes one [1] webcoket client connetion
    '''
    def __init__(self):
        self.ws_server = None
        self.last_change_time = None
        self.servo_controller = ServoController()
        self.notes_index = 0
        self.current_phase = 1
        self.secs_per_note = 1
        self.secs_per_note_empty = 3
        self.flute_listener = FluteListener()
        self.flute_listener.start()
        self.current_ws = None

    def start(self):
        '''
        '''

        print(f"[MainServer] Run socket listener on {WEBSOCKET_IP}:{PORT}")
        self.ws_server = websockets.serve(self._listen, WEBSOCKET_IP, PORT)
        asyncio.get_event_loop().run_until_complete(self.ws_server)
        asyncio.get_event_loop().run_forever()

    def get_note_perc(self):
        if self.current_note_empty:
            return (time.time() - self.last_change_time)/self.secs_per_note_empty
        else:
            return (time.time() - self.last_change_time)/self.secs_per_note

    def get_correct_positions(self, notes):
        res = []
        for note in notes:
            res.append(NOTE_TO_SERVO_MAP[note])
        return res

    async def _eager_send(self, websocket, msg):
        # returns contorl to event loop and forces message out
        await websocket.send(msg)
        await asyncio.sleep(0)

    def _err_msg(self, websocket, msg):
        data = {
            'status': 'error',
            'msg': msg
        }
        websocket.send(json.dump(data))

    async def _listen(self, websocket, path):
        '''
        A router
        '''
        path_map = {
            'tempo': self._ws_handle_tempo,
            'change-phase': self._ws_handle_phase,
            'test-practice': self._ws_handle_test_phase,
        }

        try:
            while True:
                request = await websocket.recv()
                print(request)
                try:
                    request = json.loads(request)
                except Exception as e:
                    print("[MainServer] Not json format: ", request)
                    self._err_msg(websocket, 'Invalid Format')
                    continue

                payload_path = request.get('path')
                handle_method = path_map.get(payload_path, None)
                if handle_method:
                    print(f"[MainServer] Got path {path}")
                    await handle_method(websocket, request)
                else:
                    print("[MainServer] Unknown request: ", payload_path)

        except websockets.exceptions.ConnectionClosed as cc_except:
            print(f"[MainServer] Client WS connection closed: {cc_except}")
            await websocket.close()

        except asyncio.streams.IncompleteReadError as err:
            # Handles the internal asyncio.streams.IncompleteReadError error
            # which occurs with message: 0 bytes read on a total of 2 expected
            # bytes. This appears to be caused by an empty message received in
            # the call to websocket.recv() above. The method Websockets uses is
            # asyncio.StreamReader.readexactly. The method does exactly what it
            # says and so causes the error when an empty message is recieved.
            # Not sure if this is from a bug in this code or upstream in
            # websocket code.
            print(f"[MainServer] Error reading from client WS: {err}")
            await websocket.close()

    async def _ws_handle_phase(self, websocket, request):
        if request.get('data') == 'phase-1':
            self.current_phase = 1
        elif request.get('data') == 'phase-2':
            self.current_phase = 2
        elif request.get('data') == 'phase-3':
            self.current_phase = 3

    async def _ws_handle_tempo(self, websocket, request):
        print('[MainServer][_ws_handle_tempo]')
        if request.get('data') == 'get-current-tempo':
            await websocket.send(json.dumps({
                    'currentTempo': str(self.secs_per_note)
                }))
        elif request.get('data') == 'increase':
            new_tempo = round(max(self.secs_per_note - 0.2, 0.8), 1)
            self.secs_per_note = new_tempo
            print(f'new_tempo: {self.secs_per_note}')
            if new_tempo == 0.8:
                await websocket.send('tempo-max')
            else:
                await websocket.send('tempo-ok')

        elif request.get('data') == 'decrease':
            new_tempo = round(min(self.secs_per_note + 0.2, 3), 1)
            self.secs_per_note = new_tempo
            print(f'new_tempo: {self.secs_per_note}')
            if new_tempo == 3:
                await websocket.send('tempo-min')
            else:
                await websocket.send('tempo-ok')

    async def _ws_handle_test_phase(self, websocket, request):
        if request.get('data') == 'reset':
            self.notes_index = 0
            return
        
        if request.get('data') == 'start_test':
            mode = 'test'
        else:
            mode = 'practice'

        print('[MainServer][_ws_handle_test_phase]')
        self.test_progress = {
            'status': 'start',
        }
        await websocket.send('start')
        if mode == 'test':
            time.sleep(2)
            if self.current_phase == 1:
                notes_to_learn = phase_1_notes[self.notes_index]
                phase_notes_count = len(phase_1_notes)
            elif self.current_phase == 2:
                notes_to_learn = phase_2_notes[self.notes_index]
                phase_notes_count = len(phase_2_notes)
            elif self.current_phase == 3:
                notes_to_learn = phase_3_notes[self.notes_index]
                phase_notes_count = len(phase_3_notes)
            else:
                raise Exception('Incorrect Phase')
            self.notes_index += 1
            self.servo_controller.play_score(notes_to_learn)
            self.servo_controller.reset()
            time.sleep(2)
            await websocket.send('start_playback')
            time.sleep(1)
        else:
            time.sleep(2)
            notes_to_learn = [0 for x in range(6)]
            await websocket.send('start_playback')
        
        user_ans = []
        self.last_change_time = time.time()
        prev_temp_ans = None
        prev_msg_time = time.time() - 100
        while len(user_ans) < len(notes_to_learn):
            temp_ans = self.flute_listener.get_current_positions()
            if temp_ans == [0, 0, 0, 0, 0, 0]:
                self.current_note_empty = True
            else:
                self.current_note_empty = False
            note_perc = self.get_note_perc()
            if temp_ans != prev_temp_ans or time.time() - prev_msg_time > 0.25:
                if temp_ans != prev_temp_ans:
                    self.last_change_time = time.time()
                res = user_ans + [temp_ans]
                msg = json.dumps({
                    'fingerPositions': res,
                    'cursorPosition': note_perc,
                })
                await self._eager_send(websocket, msg)
                prev_temp_ans = temp_ans
                prev_msg_time = time.time()
            # move to next note after X secs
            if note_perc > 1:
                user_ans.append(temp_ans)
                self.last_change_time = time.time()
            time.sleep(0.1)
        
        # All done with answers, return
        await websocket.send('playback_complete')
        if mode == 'test':
            correct_positions = self.get_correct_positions(notes_to_learn)
            await websocket.send(json.dumps({
                'correctPositions': correct_positions
            }))
        # TODO: LOG
        if mode == 'test':
            # convert to same 0 , 1 , .. format
            _correct_positions_bi = [[1 if x in res_i else 0 for x in range(6)] for res_i in correct_positions]
            log_data = {
                'user_ans': user_ans,
                'correctpositions': _correct_positions_bi
            }
            filename = os.path.join(
                LOG_DIR,
                f'phase_{self.current_phase}_index_{self.notes_index}.json'
            )
            with open(filename, 'w') as f:
                json.dump(log_data, f, indent=4)
        if mode == 'test':
            if phase_notes_count == self.notes_index:
                await websocket.send('phase_complete')


if __name__ == '__main__':
    MainServer().start()
