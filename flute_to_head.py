import serial
import threading
import time
import queue

from controller import (
    ServoController, NOTE_TO_SERVO_MAP
)

'''
sudo rfcomm release all
sudo rfcomm bind 0 00:14:03:05:08:7F
'''

btSerial = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=0.5)
btSerial.write(b"Hi")

servo_controller = ServoController()
servo_controller.reset()

# thread and queue
# one thread to listen to bt serial and add message to queue
# another to handle data in queue


def listener(q):
    print('-- starting bt listener --')
    btSerial.write(b"Hi")
    while True:
        data = btSerial.readline()
        if not data:
            time.sleep(0.1)
            continue
        print('got data')
        q.put(data)


def main():
    q = queue.Queue()
    threading.Thread(
        target=listener,
        args=(q, )
    ).start()
    while True:
        msg = q.get()
        print(msg)
        servo_controller.move_arms_by_bt(msg)


if __name__ == '__main__':
    main()
