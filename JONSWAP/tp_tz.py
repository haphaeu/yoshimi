# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 16:12:28 2016

@author: rarossi
"""

from math import sqrt, exp


def jonswap_gamma_DNVH103(hs, tp):
    """JONSWAP gamma as per DNV-H103"""
    if hs < 0.1: return 1.0
    alpha = tp/sqrt(hs)
    if alpha >= 3.6 and alpha <= 5.0:
        return exp(5.75-1.15*alpha)
    if alpha < 3.6:
        return 5.0
    if alpha > 5.0:
        return 1.0


def jonswap_tz_DNVH103(hs, tp):
    """Convert Tp into Tz for a given Hs.
    Using gamma from DNV-RP-H103.
    """
    gamma = jonswap_gamma_DNVH103(hs, tp)
    return tp * (0.6673 + 0.05037*gamma - 0.006230*gamma**2 + 0.0003341*gamma**3)


def jonswap_tp_DNVH103(hs, tz):
    """Convert Tz into Tp for a given Hs."""
    tp0 = tz
    delta = 1.0
    err, err0, i, maxiter = 1, 1, 0, 9999
    while i < maxiter:
        err = tz - jonswap_tz_DNVH103(hs, tp0)
        if abs(err) < 1e-12:
            return tp0
        if err > 0:
            tp0 += delta
        else:
            tp0 -= delta
        if err/err0 < 0:
            delta /= 2.0
        err0 = err
        i += 1
    print('Reached maximum number of iterations. Error:', err)
    return tp0


if __name__ == '__main__':
    hs_tz = [(1.75, 5), (2.00, 6), (2.50, 7), (2.50, 9),
             (3.00, 10), (3.00, 13), (3.50, 14), (3.50, 15)]

    for hs, tz in hs_tz:
        tp = jonswap_tp_DNVH103(hs, tz)
        print(hs, tz, tp, tz-jonswap_tz_DNVH103(hs, tp))

