import argparse
import sys
import time

from controller import (
    ServoController, NOTE_TO_SERVO_MAP
)

from collections import Counter
import random


# order matters
KEYBOARD_KEYS = ['m', 'n', 'b', '3', '2', '1']
# # C
#  0: [0, 1, 2, 3, 4, 5],

# # D
# 2: [0, 1, 2, 3, 4],

# # E
# 4: [0, 1, 2, 3],

# # F
# 5: [0, 1, 2],

# # G
# 7: [0, 1],
# # A
# 9: [0],
# # B
# 11: [],


'''
C D E F G A B
0 2 4 5 7 9 11
'''


# 'eighth': BASE_UNIT,
# 'quarter': BASE_UNIT * 2,
# 'half': BASE_UNIT * 4,
# half+: BASE_UNIT * 6,
# 'whole': BASE_UNIT * 8

ALL_SONGS = [
    # Song 0 - piece no. 1
    [
        (0, 'quarter'), (7, 'quarter'), (9, 'quarter'), (7, 'quarter'),
        (5, 'quarter'), (4, 'quarter'), (2, 'quarter'), (0, 'quarter'),
        (7, 'quarter'), (5, 'quarter'), (4, 'quarter'), (2, 'quarter'),
        (7, 'quarter'), (5, 'quarter'), (4, 'quarter'), (2, 'quarter'),
        (0, 'quarter'), (7, 'quarter'), (9, 'quarter'), (7, 'quarter'),
        (5, 'quarter'), (4, 'quarter'), (2, 'quarter'), (0, 'quarter'),
    ],
    # Song 1 - piece no. 4
    [
        (4, 'half'), (5, 'quarter'), (7, 'half'),
        (5, 'quarter'), (4, 'quarter'), (2, 'quarter'), (0, 'half'),
        (2, 'quarter'), (4, 'half'), (2, 'half+'),
        (4, 'half'), (5, 'quarter'), (7, 'half'),
        (5, 'quarter'), (4, 'quarter'), (2, 'quarter'), (0, 'half'),
        (2, 'quarter'), (4, 'quarter'), (2, 'half'), (0, 'half'),
    ],

]


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


def test_song(song_index):
    group_size = 4
    notes_to_learn = ALL_SONGS[song_index]
    notes_by_group = []
    tmp_group = []
    for i in range(len(notes_to_learn)):
        tmp_group.append(notes_to_learn[i])
        if len(tmp_group) == group_size:
            notes_by_group.append(tmp_group)
            tmp_group = []

    servo_controller = ServoController()

    for note_group in notes_by_group:
        stay_in_group = True
        while stay_in_group:
            print('Playing notes to learn ...')
            time.sleep(2)
            servo_controller.play_score(note_group)
            servo_controller.reset()
            time.sleep(2)
            user_ans = input('r/R to repeat. n/N for next group. Or input other to test yourself.\n').strip()
            if user_ans.lower() == 'r':
                stay_in_group = True
            elif user_ans.lower() == 'n':
                stay_in_group = False
            else:
                stay_in_group = False
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
                    fingers = input_to_fingers(user_ans)
                    user_answers.append(fingers)

                # print results
                for i in range(group_size):
                    note = note_group[i][0]
                    ans = user_answers[i]
                    correct_fingers = NOTE_TO_SERVO_MAP[note]
                    print(f"Correct   :  {fingers_to_display(correct_fingers)}")
                    print(f"User Input:  {fingers_to_display(ans)}")
                    print('\n')


if __name__ == '__main__':
    '''
    python test_songs.py --song_index=1
    '''

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--song-index',
        type=int,
        default=0,
        help='Which song?'
    )

    args = parser.parse_args()
    test_song(song_index=args.song_index)
