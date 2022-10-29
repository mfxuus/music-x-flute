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


class ServoController:
    '''
    for testing on PC
    '''
    def reset(self):
        print('resetting DummyServoController')

    def play_score(self, notes_to_learn):
        print('play_score:', notes_to_learn)