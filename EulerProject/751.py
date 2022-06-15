# https://projecteuler.net/problem=751

# Tried without the Decimal, it does not converge.

import time
from decimal import Decimal
from math import floor, log10

VERB = True


def seq_a(theta, max_iters=99):
    """Return an iterator that gives the sequence a_n"""
    b = theta
    a = floor(b)
    yield a
    for i in range(max_iters):
        b = floor(b) * (b - floor(b) + 1)
        a = floor(b)
        yield a


def concat(seq):
    """Return tau, the concatenation of sequence a_n."""
    loc = -1
    x = Decimal(0)
    for a in seq:
        digits = 1 + int(log10(a))
        loc += digits
        d = Decimal(a) / Decimal(10**loc)
        x += d
    return x


def main():
    """Starting at 2, calculate and concatenate a_n
    and use output tau as new input theta. 
    Convergence is achieved quickly.
    """
    x0 = Decimal(2)
    if VERB: print(f'{x0:.24f}')
    eps=Decimal('1e-24')
    for i in range(99):
        seq = list(seq_a(x0, 25))
        x1 = concat(seq)
        if VERB: print(f'{x1:.24f}')
        if abs(x1 - x0) < eps:
            if VERB: print(f'Converged after {i + 1} interactions.')
            break
        x0 = x1
    return x1


if __name__ == '__main__':
    t0 = time.time()
    x = main()
    et = time.time() - t0
    if VERB: print(f'et: {et}')

"""
2.000000000000000000000000
2.222222222222222222222222
2.223569173365129257513103
2.223561019324056851562705
2.223561019313554106181352
2.223561019313554106173177
2.223561019313554106173177
Converged after 6 interactions.
et: 0.0040018558502197266
"""