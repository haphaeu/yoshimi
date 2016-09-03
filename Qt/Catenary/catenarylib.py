# -*- coding: utf-8 -*-
"""

Catenary Lib
============

Solvers for catenary equations with touch down.

The functions below solve the catenary equation (with touch down), given any
2 parameters. All functions return a tuple with all 5 catenary parameters:
TA, V, H, L, MBR

This is an upgrade to Python/PyQt4 of the old app written back in 2010 using MS VBA

Created on Wed Sep 03

@author: raf
"""

from math import pi, tan, cos, asinh


def CatenaryCalcTAV(TA, V):
    """CatenaryCalcTAV(TA, V) -> TA, V, H, L, MBR"""
    # top angle w horizontal, in radians
    theta = (90 - TA) * pi / 180
    # minimum bend radius
    MBR = V * cos(theta) / (1 - cos(theta))
    # curvilinear length
    L = MBR * tan(theta)
    # horizontal distance
    H = MBR * asinh(tan(theta))
    # return catenary parameters
    return TA, V, H, L, MBR


def CatenaryCalcTAH(TA, H):
    """CatenaryCalcTAH(TA, H) -> TA, V, H, L, MBR"""
    # top angle w horizontal, on radians
    theta = (90 - TA) * pi / 180
    # minimum bend radius
    MBR = H / asinh(tan(theta))
    # vertical distance
    V = MBR / (cos(theta) / (1 - cos(theta)))
    # curvilinear length
    L = MBR * tan(theta)
    return TA, V, H, L, MBR


def CatenaryCalcTAL(TA, L):
    """CatenaryCalcTAL(TA, L) -> TA, V, H, L, MBR"""
    # top angle w horizontal, on radians
    theta = (90 - TA) * pi / 180
    # minimum bend radius
    MBR = L / tan(theta)
    # vertical distance
    V = MBR / (cos(theta) / (1 - cos(theta)))
    # horizontal distance
    H = MBR * asinh(tan(theta))
    return TA, V, H, L, MBR


def CatenaryCalcTAMBR(TA, MBR):
    """CatenaryCalcTAMBR(TA, MBR) -> TA, V, H, L, MBR"""
    # top angle w horizontal, on radians
    theta = (90 - TA) * pi / 180
    # vertical distance
    V = MBR / (cos(theta) / (1 - cos(theta)))
    # curvilinear length
    L = MBR * tan(theta)
    # horizontal distance
    H = MBR * asinh(tan(theta))
    return TA, V, H, L, MBR


def CatenarySolveL_MBR(L, MBR):
    """CatenarySolveL_MBR(L, MBR) -> TA, V, H, L, MBR"""
    TAi = 0.0
    delta = 1.0
    tolerance = 0.0000001
    TAi = TAi + delta
    erro = CatenaryCalcTAL(TAi, L)[4] - MBR
    while abs(erro) > tolerance:
        TAi += delta
        erroi = CatenaryCalcTAL(TAi, L)[4] - MBR
        if erro * erroi < 0:
            TAi -= delta
            delta /= 2
        else:
            erro = erroi
    return CatenaryCalcTAL(TAi, L)


def CatenarySolveH_LMBR(H, param, flag='L'):
    """CatenarySolveH_LMBR(H, param, flag) -> TA, V, H, L, MBR
    if flag == 'L':
        CatenarySolveH_LMBR(H, L, 'L') -> TA, V, H, L, MBR
    if flag == 'MBR':
        CatenarySolveH_LMBR(H, MBR, 'MBR') -> TA, V, H, L, MBR
    """
    TAi = 0.0
    delta = 1.0
    tolerance = 0.0000001
    TAi += delta
    if flag.upper() == 'L':
        idx = 3
    elif flag.upper() == 'MBR':
        idx = 4
    else:
        return 1/0  # force error
    erro = CatenaryCalcTAH(TAi, H)[idx] - param
    while abs(erro) > tolerance:
        TAi += delta
        erroi = CatenaryCalcTAH(TAi, H)[idx] - param
        if erro * erroi < 0:
            TAi -= delta
            delta /= 2
        else:
            erro = erroi
    return CatenaryCalcTAH(TAi, H)


def CatenarySolveV_HLMBR(V, param, flag='H'):
    """CatenarySolveV_HLMBR(V, param, flag) -> TA, V, H, L, MBR
    if flag == 'H':
        CatenarySolveV_HLMBR(V, H, 'H') -> TA, V, H, L, MBR
    if flag == 'L':
        CatenarySolveV_HLMBR(V, L, 'L') -> TA, V, H, L, MBR
    if flag == 'MBR':
        CatenarySolveV_HLMBR(V, MBR, 'MBR') -> TA, V, H, L, MBR
    """
    TAi = 0.0
    delta = 1.0
    tolerance = 0.0000001
    TAi += delta
    if flag.upper() == 'H':
        idx = 2
    elif flag.upper() == 'L':
        idx = 3
    elif flag.upper() == 'MBR':
        idx = 4
    else:
        return 1/0  # force error

    erro = CatenaryCalcTAV(TAi, V)[idx] - param
    while abs(erro) > tolerance:
        TAi += delta
        erroi = CatenaryCalcTAV(TAi, V)[idx] - param
        if erro * erroi < 0:
            TAi -= delta
            delta /= 2
        else:
            erro = erroi
    return CatenaryCalcTAV(TAi, V)


def unit_tests():
    """Tests all catenary functions for a known solution."""
    from numpy import allclose
    TA, V, H, L, MBR = (12, 1800, 1064.3904537756875,
                        2222.8148817630927, 472.47388849652003)
    if all((allclose((TA, V, H, L, MBR), CatenaryCalcTAV(TA, V)),
           allclose((TA, V, H, L, MBR), CatenaryCalcTAH(TA, H)),
           allclose((TA, V, H, L, MBR), CatenaryCalcTAL(TA, L)),
           allclose((TA, V, H, L, MBR), CatenaryCalcTAMBR(TA, MBR)),
           allclose((TA, V, H, L, MBR), CatenarySolveH_LMBR(H, L, flag='L')),
           allclose((TA, V, H, L, MBR), CatenarySolveH_LMBR(H, MBR, flag='MBR')),
           allclose((TA, V, H, L, MBR), CatenarySolveV_HLMBR(V, H, flag='H')),
           allclose((TA, V, H, L, MBR), CatenarySolveV_HLMBR(V, L, flag='L')),
           allclose((TA, V, H, L, MBR), CatenarySolveV_HLMBR(V, MBR, flag='MBR')))):
        return True
    else:
        return False


if __name__ == '__main__':
    if unit_tests():
        print('Unit tests: passed')
    else:
        print('Unit tests: failed.')
