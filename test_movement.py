import argparse
import sys
import time

from controller import ServoController
from collections import Counter
import random


# servo_controller = ServoController()
# for i in range(6):
#     print(f'This is arm {i}')
#     servo_controller.swing_arms_t([i], 3)
#     time.sleep(3)

def random_movements(arms_count, sc):
    arms = [0, 1, 2, 3, 4, 5]
    chosen_arms = set(random.sample(arms, arms_count))
    move_back = False
    if random.random() > 0.6:
        move_back = True
    sc.swing_arms_t(chosen_arms, stay_time=0.1, move_back=move_back)
    time.sleep(0.5)


def test_pull_push(rounds=20):
    servo_controller = ServoController()
    record = {
        'push_count': 0,
        'push_correct': 0,
        'pull_count': 0,
        'pull_correct': 0,
    }
    for _round in range(rounds):
        for i in range(10):
            random_movements(random.randint(1, 5), servo_controller)
            time.sleep(0.2)
        time.sleep(2)
        print('Prepare for test ...')
        time.sleep(1)
        # pick a random arm
        arm = random.randint(0, 5)
        # check current arm position
        servo = servo_controller.servo_map[arm]
        current_servo_pos = servo.angle
        if current_servo_pos < 10:
            action = 'push'
            # servo.angle = 80
            servo_controller.swing_arms_t([arm], stay_time=0.1, move_back=False)
            record['push_count'] += 1
        else:
            action = 'pull'
            servo.angle = 0
            record['pull_count'] += 1
        user_ans = input('Push (1) or Pull (0)? \n').strip()
        if action == 'push' and int(user_ans) == 1:
            print('Correct!')
            record['push_correct'] += 1
        elif action == 'pull' and int(user_ans) == 0:
            print('Correct!')
            record['pull_correct'] += 1
        else:
            print('Incorrect!')
    print(record)


def test_single_arm(rounds=20):
    def _print_results(correct_arr, answ_arr):
        correct_arms = []
        wrong_arms = []
        correct_count = 0
        i = 0
        for item in correct_arr:
            res = 'Correct' if (answ_arr[i] == item) else 'Wrong'
            if res == 'Correct':
                correct_count += 1
                correct_arms.append(item)
            else:
                wrong_arms.append(item)
            print(f'Round {i+1}: {res}; Moved: {item}; User Answer: {answ_arr[i]}')
            i += 1
        print(f'Score: {correct_count}/{len(correct_arr)}')
        correct_counter = Counter(correct_arms)
        wrong_counter = Counter(wrong_arms)
        for i in range(6):
            _correct = correct_counter.get(i, 0)
            _total = _correct + wrong_counter.get(i, 0)
            print(f'Arm {i} score: {_correct}/{_total}')
    servo_controller = ServoController()
    move_hist = []
    user_hist = []
    user_ans = None
    arms = [0, 1, 2, 3, 4, 5]
    print(f'Starting test of {rounds} rounds. Enter q to quit. r to repeat.')
    for i in range(rounds):
        chosen_arm = random.choice(arms)
        servo_controller.swing_arms_t([chosen_arm])
        while True:
            user_ans = input('Which arm [0-5] moved? \n').strip()
            if user_ans == 'q':
                print('Quitting test...')
                _print_results(move_hist, user_hist)
                return
            elif user_ans == 'r':
                print('Repeating...')
                servo_controller.swing_arms_t([chosen_arm])
                continue
            try:
                user_ans = int(user_ans)
                if user_ans not in arms:
                    raise
                else:
                    break
            except:
                print('Invalid answer. Please enter values between 0 and 5.')
                continue

        move_hist.append(chosen_arm)
        user_hist.append(user_ans)

    _print_results(move_hist, user_hist)


def test_two_arms(rounds=20):
    arms_moving = 2
    def _print_results(correct_arr, answ_arr):
        score_record = {}
        i = 0
        for item in correct_arr:
            user_ans = answ_arr[i]
            score = len(user_ans.intersection(item)) / arms_moving
            key = tuple(sorted(tuple(item)))
            user_ans = tuple(sorted(tuple(user_ans)))
            if key not in score_record:
                score_record[key] = [score]
            else:
                score_record[key].append(score)
            print(f'Round {i+1}: Score: {score}; Moved: {key}; User Answer: {user_ans}')
            i += 1
        total_score = 0
        avg_score_record = {}
        for k, v in score_record.items():
            sum_for_key = sum(score_record[k])
            count_for_key = len(score_record[k])
            total_score += sum_for_key
            avg_score_record[k] = round(sum_for_key/count_for_key, 4)
        print(f'Overall Average Score: {total_score/rounds}')
        for k, v in avg_score_record.items():
            print(f"Arm combo {k} score: {v}")
    servo_controller = ServoController()
    move_hist = []
    user_hist = []
    user_ans = None
    arms = [0, 1, 2, 3, 4, 5]
    print(f'Starting test of {rounds} rounds. Enter q to quit. r to repeat.')
    for i in range(rounds):
        chosen_arms = set(random.sample(arms, 2))
        servo_controller.swing_arms_t(chosen_arms)
        while True:
            user_ans = input('Which two arms [0-5] moved? (ex: 0 4)\n').strip()
            if user_ans == 'q':
                print('Quitting test...')
                _print_results(move_hist, user_hist)
                return
            elif user_ans == 'r':
                print('Repeating...')
                servo_controller.swing_arms_t(chosen_arms)
                continue
            try:
                user_ans = [int(x) for x in user_ans.split(' ')]
                user_ans = set(user_ans)
                for x in user_ans:
                    if x not in arms:
                        raise
                else:
                    break
            except:
                print('Invalid answer. Please enter values between 0 and 5.')
                continue

        move_hist.append(chosen_arms)
        user_hist.append(user_ans)

    _print_results(move_hist, user_hist)


if __name__ == '__main__':
    '''
    python test_movement.py --arms=2 --rounds=50
    '''

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--arms',
        type=int,
        default=1,
        help='Number of arms'
    )

    parser.add_argument(
        '--type',
        type=str,
        default='',
        help='Which test?'
    )

    parser.add_argument(
        '--rounds',
        type=int,
        default=20,
        help='Number of rounds'
    )

    args = parser.parse_args()

    if args.type == 'pull_push':
        test_pull_push(args.rounds)

    else:
        if args.arms not in [1, 2]:
            print("arms must be 1 or 2")
            sys.exit()

        if args.arms == 1:
            test_single_arm(rounds=args.rounds)
        elif args.arms == 2:
            test_two_arms(rounds=args.rounds)
