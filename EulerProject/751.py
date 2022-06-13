# https://projecteuler.net/problem=751

# Tried without the Decimal, it does not converge.

import sys
import time
import numpy as np
from decimal import Decimal
from math import floor, log10
import matplotlib.pyplot as plt


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
        if False:
             print('%4d' % a, f'{x:.{loc}f}', f'{d:.{loc}f}')
    return x


def interval(a, b):
    """Calculates thetas and taus in a given internal [a, b]."""
    n = 10
    delta = Decimal(b - a) / Decimal(n-1)
    thetas = [a + delta * Decimal(i) for i in range(n)]
    taus = []
    for theta in thetas:
        print(theta, end='\r')
        it = seq_a(theta)
        seq = []
        for x in it:
            seq.append(x)
            precision = len(''.join([str(a) for a in seq[1:]]))
            if precision > 25:
                break
        tau = concat(seq)
        taus.append(tau)
        
    return thetas, taus


def search(a, b):
    """Return a sub-set of an interval [a, b] containing the root theta == tau."""
    thetas, taus = interval(a, b)
    diff = np.array(thetas) - np.array(taus)
    idx = diff[diff < 0].size
    a, b = thetas[idx-1:idx+1]
    return a, b


def main():
    """Starting at [2.1, 2.9], gradually reduces the interval
    until 25 digits precision is met.
    """
    a, b = Decimal(2.1), Decimal(2.9)
    eps = Decimal(1e-25)
    max_iters=100

    for i in range(max_iters):
        a, b = search(a, b)
        print(f'{a:.24f}, {b:.24f}', end='\r')
        if abs(a - b) < eps:
            print(f'\nReached tolerance after {i} interactions.')
            break
    else:
        print('\nReached max iters')


if __name__ == '__main__':
    t0 = time.time()
    main()
    et = time.time() - t0
    print(f'et: {et}')

"""
Answer is
2.223561019313554106173177

2.223561019313554106173177, 2.223561019313554106173177
Reached tolerance after 26 interactions.
et: 0.05208015441894531
"""