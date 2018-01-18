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

from math import pi, tan, cos, asinh, radians


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
    """
    CatenarySolveH_LMBR(H, param, flag) -> TA, V, H, L, MBR

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
    """
    CatenarySolveV_HLMBR(V, param, flag) -> TA, V, H, L, MBR
        Solve catenary parameters given V and either H, L or MBR.

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


def CatenaryOffset(params, DeltaH=0, DeltaV=0):
    """CatenaryOffset(params, DeltaH, DeltaV) -> TA, V, H, L, MBR

    Apply an offset to the top of the catenary.
    """

    TA, V, H, L, MBR = params

    # Check if input values are reasonable
    UpperBoundDeltaH = 0.2 * V
    LowerBoundDeltaH = -min(0.2 * V, H / 2)
    UpperBoundDeltaV = min(50, V / 10)
    LowerBoundDeltaV = -UpperBoundDeltaV
    UpperBoundTA = 75
    LowerBoundTA = 2

    if DeltaH > UpperBoundDeltaH:
        print("Maximum offset restraint to 20% of the depth.")
        return
    elif DeltaH < LowerBoundDeltaH:
        print("Minimum offset restraint to 20% of the depth or 50% of the horizontal length.")
        return
    elif DeltaV > UpperBoundDeltaV or DeltaV < LowerBoundDeltaV:
        print("Vertical excursions restraint to either 50m or 10% of depth, whichever is smaller.")
        return
    elif TA > UpperBoundTA and (DeltaH > 0 or DeltaV > 0):
        print("Far offsets and upwards excursions not allowed for top angles > 75deg")
        return
    elif TA < LowerBoundTA and (DeltaH < 0 or DeltaV < 0):
        print("Near offsets and downwards excursions not allowed for top angles < 2deg")
        return

    # Data for "offset" SCR
    Vo = V + DeltaV

    # Newton solver to find root of functions

    delta = 0.1  # delta TA to estimate derivative
    tolerance = 0.01
    f_TA = 999
    i = 0
    TAo = TA  # initial guess for TA
    while abs(f_TA) > tolerance:
        i += 1
        # Calculate f(TAo-delta)
        retval = CatenaryCalcTAV(TAo - delta, Vo)
        Ho = retval[2]
        Lo = retval[3]
        f_TA_menos_delta = L - Lo - H + Ho - DeltaH
        # calculate f(TAo+delta)
        retval = CatenaryCalcTAV(TAo + delta, Vo)
        Ho = retval[2]
        Lo = retval[3]
        f_TA_mais_delta = L - Lo - H + Ho - DeltaH
        # calculare derivative
        f_linha = (f_TA_mais_delta - f_TA_menos_delta) / delta
        # calculate f(TAo)
        retval = CatenaryCalcTAV(TAo, Vo)
        Ho = retval[2]
        Lo = retval[3]
        f_TA = L - Lo - H + Ho - DeltaH
        # Newton-Raphson Iteration
        TAo = TAo - f_TA / f_linha

    MBRo = retval[4]
    return TAo, Vo, Ho, Lo, MBRo


def unit_tests():
    """Test all catenary functions for a known solution."""
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
           allclose((TA, V, H, L, MBR), CatenarySolveV_HLMBR(V, MBR, flag='MBR')),
           allclose((TA, V, H, L, MBR),
                    CatenaryOffset(CatenaryOffset(CatenaryCalcTAV(TA, V), -5, 5), 5, -5)))):
        return True
    else:
        return False


def reactions(TA, L, w):
    """
    `reactions(TA, L, w) -> (Fh, Fv, F)`
        Reaction forces due to catenary weight.

    Parameters
    ----------
    TA : float
        top angle with vertical, in degrees.
    L : float
        length of suspended line, im meters.
    w : float
        unit weight of line, in kg/m
    Output
    ------
    (Fh, Fv, F) : tuple of floats, in kN
        Horizontal, vertical and total reaction force at the top of the line
        due to self weight.
    """
    mg = 9.80665/1000
    Fv = w * L * mg
    Fh = Fv * tan(radians(TA))
    F = Fv / cos(radians(TA))
    return Fh, Fv, F


if __name__ == '__main__':
    if unit_tests():
        print('Unit tests: passed')
    else:
        print('Unit tests: failed.')
