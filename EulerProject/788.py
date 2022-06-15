# https://projecteuler.net/problem=788

import time
from math import log10, comb


def is_dominating_str(n):
    nstr = str(n)
    size = len(nstr)
    required = size // 2 + 1
    digits = set(nstr)
    ndigits = len(digits)
    max_digits = size - required + 1
    if ndigits > max_digits:
        return False
    for d in digits:
        if nstr.count(d) >= required:
            return True
    return False

def is_dominating(n):
    # ## DOES NOT WORK!!!
    ndigits = 1 + int(log10(n))
    digits_list = [0] * ndigits
    i = 0
    while n > 0:
        digits_list[i] = n % 10
        n = n // 10
        i += 1
    digits_set = set(digits_list)
    n_unique_digits = len(digits_set)
    threshold = ndigits // 2 + ndigits % 2
    if n_unique_digits < threshold:
        return True
    elif n_unique_digits > threshold:
        return False
    else:  # n_unique_digits == threshold:
        required = ndigits // 2 + 1
        for d in digits_set:
            if digits_list.count(d) >= required:
                return True
        return False


def D_old(N):
    count = 0
    for n in range(1, 10**N):
        if is_dominating_str(n):
            count += 1
    return count



def D(N):
    count = 0
    for n in range(1, N + 1):
        # Required number of equal digits 
        # for the number to be dominating
        required = n // 2 + 1
        rest = n - required
        count += sum([comb(n, r) * 9**(r + 1) for r in range(rest + 1)])
    return count


if __name__ == '__main__':
    print(f'D(4) = {D(4)}')
    print(f'D(10) = {D(10)}')
    t0 = time.time()
    print(f'D(2022) modulo 1_000_000_007 = {D(2022) % 1_000_000_007}')
    et = time.time() - t0
    print(f'et: {et}')