"""
https://en.wikipedia.org/wiki/Monty_Hall_problem
"""

from random import randint


def turn(switch=True):
    gold_at = randint(1, 3)
    guess = randint(1, 3)
    if not switch:
        return guess == gold_at
    else:
        return not guess == gold_at


def calc(num_turns, switch):
    turns = [turn(switch) for i in range(num_turns)]
    num_turns_won = sum(turns)
    return num_turns_won


def main(series=3):
    num_turns=10000
    print('Switching:')
    for s in range(series):
        num_turns_won = calc(num_turns, switch=True)
        print(f'  ({s+1}) Won {100*num_turns_won/num_turns:.1f}%')
    print('Not switching:')
    for s in range(series):
        num_turns_won = calc(num_turns=10000, switch=False)
        print(f'  ({s+1}) Won {100*num_turns_won/num_turns:.1f}%')

if __name__ == '__main__':
    main()