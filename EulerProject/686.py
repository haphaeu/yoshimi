"""Project Euler - problem 686

2^7=128 is the first power of two whose leading digits are "12".

The next power of two whose leading digits are "12" is 2^80.

Define p(L, n) to be the nth-smallest value of j such that the base 10 
representation of 2^j begins with the digits of L.

So p(12, 1) = 7 and p(12, 2) = 80.

You are also given that p(123, 45) = 12710

Find p(123, 678910).

https://projecteuler.net/problem=686

--- Solution ---

2^j = 123... can be writen as 1.23... * 10^k, for a certain k.

So we know that (using log10):

    1.23 * 10^k < 2^j < 1.24 * 10^k

    (log(1.23) + k) / log(2) < j < (log(1.24) + k) / log(2)

Restricted that both k and j must be integers. So if we iterate
over integer values of k, we can calculate j for both sides of the
inequality, and only consider values where there is an integer
in between, ie:

    j1 = (log(1.23) + k) / log(2)
    j2 = (log(1.24) + k) / log(2)

For the valid values of k, j1 is slightly below an integer, and
j2 slightly above. Hence a j is found to be int(j2).

Took some time, but it works...

got a good hint here:
https://math.stackexchange.com/a/4094026/293930

"""
from math import log10 
import time
import numba as nb


@nb.njit
def main():

    log2 = log10(2)
    log123 = log10(1.23)
    log124 = log10(1.24)

    k = 1
    c = 0
    while True:
        j1 = int((log123 + k) / log2)
        j2 = int((log124 + k) / log2)
        if j2 > j1:
            c += 1
            if c == 45:
                assert j2 == 12710
            if c == 678910:
                print(j2)
                break
        k += 1


if __name__ == '__main__':
    t0 = time.time()
    main()
    et = time.time() - t0        
    print('%.3fs' % et)

"""out:
193060223
35.582s
reduced to 1.4s with numba
"""
