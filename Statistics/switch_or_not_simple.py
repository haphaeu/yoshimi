"""
https://en.wikipedia.org/wiki/Monty_Hall_problem
"""
from random import randint as ri
N = 100_000
won = sum([not ri(1, 3) == ri(1, 3) for _ in range(N)])/N
print(f'{won:.3f}')
