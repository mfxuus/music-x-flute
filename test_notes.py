import argparse
import datetime
import json
import os
import sys
import time

from controller import (
    ServoController, NOTE_TO_SERVO_MAP
)

from collections import Counter
import random


# order matters
KEYBOARD_KEYS = ['m', 'n', 'b', '3', '2', '1']
KEYBOARD_KEYS_REVERSE = KEYBOARD_KEYS[::-1]
LOGFILE = f'{datetime.datetime.today().date()}.json'
LOGFILE = os.path.join('logs', LOGFILE)


def write_or_append_to_log(data):
    try:
        with open(LOGFILE, 'r') as f:
            _log = json.load(f)
    except Exception as e:
        print('No existing log file. Creating new one.')
        _log = []

    _log.append(data)
    with open(LOGFILE, 'w') as f:
        json.dump(_log, f, indent=4)

    print(f'LOG LENGTH: {len(_log)}')


def input_to_fingers(input_str):
    # 'mnb3' --> [0, 1, 2, 3]
    fingers = []
    i = 0
    for k in KEYBOARD_KEYS:
        if k in input_str:
            fingers.append(i)
        i += 1
    return fingers


def fingers_to_display(fingers_arr):
    out_str = ''
    for i in range(6):
        if i in fingers_arr:
            out_str += '* '
        else:
            out_str += '- '
    return out_str


def generate_notes(note_count):
    all_keys = list(NOTE_TO_SERVO_MAP.keys())
    all_keys_except_all_up = [x for x in all_keys if x != 11]
    first_note = random.choice(all_keys_except_all_up)
    remaining_count = note_count - 1
    if remaining_count > 0:
        other_notes = random.choices(all_keys, k=remaining_count)
        notes = [first_note] + other_notes
    else:
        notes = [first_note]
    return notes


def test_notes(note_count=1):
    notes_to_learn = generate_notes(note_count)

    servo_controller = ServoController()
    print('Playing notes to learn ...')
    time.sleep(2)
    servo_controller.play_score(notes_to_learn)
    servo_controller.reset()
    time.sleep(2)
    print('Time to play it back ...')
    user_answers = []
    user_answers_str = []
    user_ans = input('Enter notes (separated by 4 or v):\n').strip()
    temp_str = ''
    for char in user_ans:
        if char in KEYBOARD_KEYS + [' ']:
            temp_str += char
        elif char in ['4', 'v']:
            if temp_str:
                user_answers_str.append(temp_str)
                temp_str = ''
    user_answers_str.append(temp_str)
    for user_ans in user_answers_str:
        # auto complete lower keys
        max_input = ''
        for k in KEYBOARD_KEYS_REVERSE:
            if k in user_ans:
                max_input = k
                break

        auto_completed_ans = ''
        if max_input != '':
            for k in KEYBOARD_KEYS:
                auto_completed_ans += k
                if k == max_input:
                    break
        fingers = input_to_fingers(auto_completed_ans)
        user_answers.append(fingers)

    # print results
    notes_log = []
    for i in range(note_count):
        _temp_log = {}
        note = notes_to_learn[i]
        ans = user_answers[i]
        correct_fingers = NOTE_TO_SERVO_MAP[note]
        print(f"Correct   :  {fingers_to_display(correct_fingers)}")
        print(f"User Input:  {fingers_to_display(ans)}")
        print('\n')
        _temp_log['note'] = note
        _temp_log['user_ans'] = ans
        _temp_log['correct_answer'] = correct_fingers
        notes_log.append(_temp_log)

    write_or_append_to_log({
        'note_count': note_count,
        'notes_log': notes_log,
    })


if __name__ == '__main__':
    '''
    python test_movement.py --arms=2 --rounds=50
    '''

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--note-count',
        type=int,
        default=1,
        help='Number of notes'
    )

    args = parser.parse_args()
    test_notes(note_count=args.note_count)
