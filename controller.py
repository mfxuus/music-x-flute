import pretty_midi
import threading
import time


from board import SCL, SDA
import busio

# Import the PCA9685 module. Available in the bundle and here:
#   https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)

# Your servos
MIN_PULSE = 500
MAX_PULSE = 2500

ARM_SWING_ANGLE_1 = 60
ARM_SWING_ANGLE_2 = 80

# Where did you plug your servos?
SERVO_1_CHANNEL = 11
SERVO_2_CHANNEL = 8
SERVO_3_CHANNEL = 7
SERVO_4_CHANNEL = 4
SERVO_5_CHANNEL = 3
SERVO_6_CHANNEL = 0

# 0 back of head, 5 front of head
NOTE_TO_SERVO_MAP = {
    # C
    0: [0, 1, 2, 3, 4, 5],
    # D
    2: [0, 1, 2, 3, 4],
    # E
    4: [0, 1, 2, 3],
    # F
    5: [0, 1, 2],
    # G
    7: [0, 1],
    # A
    9: [0],
    # B
    11: [],
}

BASE_UNIT = 0.5
STAY_TIME_MAP = {
    'eighth': BASE_UNIT,
    'quarter': BASE_UNIT * 2,
    'half': BASE_UNIT * 4,
    'half+': BASE_UNIT * 6,
    'whole': BASE_UNIT * 8
}


class ServoController:
    def __init__(self):
        # Create a simple PCA9685 class instance.
        pca = PCA9685(i2c)
        # You can optionally provide a finer tuned reference clock speed to improve the accuracy of the
        # timing pulses. This calibration will be specific to each board and its environment. See the
        # calibration.py example in the PCA9685 driver.
        # pca = PCA9685(i2c, reference_clock_speed=25630710)
        pca.frequency = 60
        # how I plugged the servos?
        self.servo_map = {
            # first servo back of head
            0: servo.Servo(
                pca.channels[SERVO_1_CHANNEL],
                min_pulse=MIN_PULSE, max_pulse=MAX_PULSE),
            1: servo.Servo(
                pca.channels[SERVO_2_CHANNEL],
                min_pulse=MIN_PULSE, max_pulse=MAX_PULSE),
            2: servo.Servo(
                pca.channels[SERVO_3_CHANNEL],
                min_pulse=MIN_PULSE, max_pulse=MAX_PULSE),
            3: servo.Servo(
                pca.channels[SERVO_4_CHANNEL],
                min_pulse=MIN_PULSE, max_pulse=MAX_PULSE),
            4: servo.Servo(
                pca.channels[SERVO_5_CHANNEL],
                min_pulse=MIN_PULSE, max_pulse=MAX_PULSE),
            5: servo.Servo(
                pca.channels[SERVO_6_CHANNEL],
                min_pulse=MIN_PULSE, max_pulse=MAX_PULSE),
        }
        self.reset()
        time.sleep(1)

    # def _swing_arm(self, servo_ind, stay_time):
    #     _servo = self.servo_map[servo_ind]
    #     _servo.angle = ARM_SWING_ANGLE
    #     time.sleep(stay_time)
    #     _servo.angle = 0

    # def swing_arm_t(self, servo_ind, stay_time=0.1):
    #     t = threading.Thread(target=self._swing_arm, args=(servo_ind, stay_time, ))
    #     t.start()
    def reset(self):
        for _servo in self.servo_map.values():
            _servo.angle = 0

    def move_arms_by_bt(self, bt_command):
        '''
        bt_command: '1^2_'
        '''
        push_servos = []
        pull_servos = []
        servo_ind = None
        bt_command = bt_command.decode("utf-8")
        for char in bt_command:
            print('******')
            print(char)
            print(char == '^')
            print(char == '_')
            print(servo_ind)
            print('******')
            if char == '^' and isinstance(servo_ind, int):
                pull_servos.append(servo_ind)
                servo_ind = None
            elif char == '_' and isinstance(servo_ind, int):
                push_servos.append(servo_ind)
                servo_ind = None
            else:
                try:
                    servo_ind = int(char)
                except Exception as e:
                    print(f'Cannot cast to int: {char}')
        print('--------- move_arms_by_bt -----------')
        print(push_servos)
        print(pull_servos)
        t = threading.Thread(target=self._swing_arms, args=(
                push_servos, None, False, False, pull_servos))
        t.start()

    def _swing_arms(
            self,
            servo_ind_arr,
            stay_time,
            move_back=True,
            pull_missing_arms=False,
            pull_servo_inds=[]):
        push_servos = []
        pull_servos = []
        for servo_ind in servo_ind_arr:
            push_servos.append(self.servo_map[servo_ind])
        for servo_ind in pull_servo_inds:
            pull_servos.append(self.servo_map[servo_ind])
        if pull_missing_arms:
            for servo_ind in self.servo_map.keys():
                if servo_ind not in servo_ind_arr:
                    pull_servos.append(self.servo_map[servo_ind])
        skip_push = []
        for _servo in push_servos:
            # comment this out for small vibrations
            if _servo.angle < ARM_SWING_ANGLE_1:
                _servo.angle = ARM_SWING_ANGLE_1
            else:
                skip_push.append(_servo)
        for _servo in pull_servos:
            _servo.angle = 0

        continue_push = [servo for servo in push_servos if servo not in skip_push]
        for angle in range(ARM_SWING_ANGLE_1+2, ARM_SWING_ANGLE_2, 1):
            for _servo in continue_push:
                _servo.angle = angle
            time.sleep(0.05)

        if move_back:
            time.sleep(stay_time)
            for _servo in push_servos:
                _servo.angle = 0

    def swing_arms_t(self, servo_ind_arr, stay_time=2, move_back=True, pull_missing_arms=False):
        t = threading.Thread(target=self._swing_arms, args=(
                servo_ind_arr, stay_time, move_back, pull_missing_arms))
        t.start()

    def _play_note(self, pitch, stay_time=2, move_back=True, pull_missing_arms=True):
        note = pitch % 12
        servo_inds = NOTE_TO_SERVO_MAP.get(note)
        if servo_inds is None:
            return
        self.swing_arms_t(
            servo_inds,
            stay_time=stay_time,
            move_back=move_back,
            pull_missing_arms=pull_missing_arms
        )

    def _play_note_farthest(self, pitch, stay_time=2, move_back=True, pull_missing_arms=True):
        # only push the farthest index/finger
        note = pitch % 12
        servo_inds = NOTE_TO_SERVO_MAP.get(note)
        if servo_inds is None:
            return
        if servo_inds != []:
            servo_inds = [max(servo_inds)]
        self.swing_arms_t(
            servo_inds,
            stay_time=stay_time,
            move_back=move_back,
            pull_missing_arms=pull_missing_arms
        )

    def play_note(self, pitch, stay_time=2, move_back=True, pull_missing_arms=True):
        t = threading.Thread(target=self._play_note, args=(pitch, stay_time, move_back, pull_missing_arms))
        t.start()

    def play_score(self, notes):
        for note in notes:
            if type(note) is int:
                pitch = note
                rhythm = 'quarter'
            else:
                pitch, rhythm = note
            stay_time = STAY_TIME_MAP[rhythm]
            if pitch == 'rest':
                time.sleep(stay_time)
            else:
                # doesn't look like we need threads
                # self.play_note(note, stay_time)
                self._play_note_farthest(pitch, stay_time, False)
            time.sleep(stay_time+0.2)

    def play_midi_file(self, filepath):
        '''
        TODO: read rhythm from file too
        '''
        rhythm = 'quarter'
        midi_data = pretty_midi.PrettyMIDI(filepath)
        instrument = midi_data.instruments[0]
        notes = instrument.notes
        pitches = [note.pitch for note in notes]
        for pitch in pitches:
            stay_time = STAY_TIME_MAP[rhythm]
            if pitch == 'rest':
                time.sleep(stay_time)
            else:
                self._play_note(pitch, stay_time)
            time.sleep(0.1)





def demo_1():
    servo_controller = ServoController()
    for i in range(40):
        servo_ind = i % 6
        servo_controller.swing_arms_t([servo_ind, (servo_ind+1)%6])
        time.sleep(2)


def demo_2():
    servo_controller = ServoController()
    servo_controller.play_note(1)
    servo_controller.play_note(2, stay_time=0.5)
    servo_controller.play_note(5, stay_time=0.5)


def demo_3():
    servo_controller = ServoController()
    notes = [
        (0, 'quarter'),
        (2, 'quarter'),
        (4, 'whole'),
        ('rest', 'half'),
        (5, 'half'),
        (7, 'eighth'),
        (9, 'eighth'),
        (11, 'eighth'),
    ]
    servo_controller.play_score(notes)


def demo_4():
    servo_controller = ServoController()
    servo_controller.play_midi_file('./midi_examples/cello-C-chord.mid')


def educate():
    servo_controller = ServoController()
    print('all 6 down.')
    servo_controller.play_note(0)
    time.sleep(3)
    print('5 down.')
    servo_controller.play_note(2)
    time.sleep(3)
    print('4 down.')
    servo_controller.play_note(4)
    time.sleep(3)
    print('3 down.')
    servo_controller.play_note(5)
    time.sleep(3)
    print('2 down.')
    servo_controller.play_note(7)
    time.sleep(3)
    print('1 down.')
    servo_controller.play_note(9)
    time.sleep(3)
    print('All up.')
    servo_controller.play_note(11)


'''
from controller import ServoController
servo_controller = ServoController()
for i in range(40):
    servo_ind = i % 6
    servo_controller.swing_arm_t(servo_ind)
    servo_controller.swing_arm_t((servo_ind+1)%6)
    time.sleep(2)


servo_controller.play_note(1)
servo_controller.play_note(2, stay_time=0.5)
servo_controller.play_note(5, stay_time=0.5)


servo_controller = ServoController()
notes = [
    (1, 'quarter'),
    (1, 'quarter'),
    (2, 'whole'),
    ('rest', 'half'),
    (5, 'half'),
    (4, 'eighth'),
    (4, 'eighth'),
    (4, 'eighth'),
]
servo_controller.play_score(notes)



from controller import *
'''
