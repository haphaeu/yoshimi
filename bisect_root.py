# -*- coding: utf-8 -*-
"""
Implementation of bisection root find algorithm based on scipy implementation in C:

https://github.com/scipy/scipy/blob/v0.14.0/scipy/optimize/Zeros/bisect.c

Created on Wed Sep 27 13:51:37 2017

@author: rarossi
"""


def bisect(f, xa, xb, args=(), xtol=2e-12, rtol=8.9e-16, max_iter=100):

    tol = xtol + rtol*(abs(xa) + abs(xb))

    fa = f(xa, *args)
    fb = f(xb, *args)
    if fa*fb > 0:
        print("Error: f(xa) and f(xb) must have different signs")
        return False
    if fa == 0:
        return xa
    if fb == 0:
        return xb
    dm = xb - xa

    i = 0
    while i < max_iter:
        dm *= .5
        xm = xa + dm
        fm = f(xm, *args)
        if fm*fa >= 0:
            xa = xm
        if (fm == 0) | (abs(dm) < tol):
            return xm
    print("Error: maximum number of iterations reached.")
    return False


def unit_tests():
    """
    Modified version of:
    https://github.com/scipy/scipy/blob/v0.14.0/scipy/optimize/tests/test_zeros.py
    """
    from math import sqrt
    from numpy.testing import TestCase, assert_almost_equal, assert_
    # Import testing parameters
    from scipy.optimize._tstutils import functions, fstrings

    class TestBasic(TestCase):
        def run_check(self, method, name):
            a = .5
            b = sqrt(3)
            for function, fname in zip(functions, fstrings):
                zero = method(function, a, b, xtol=0.1e-12)
                assert_(zero)
                assert_almost_equal(zero, 1.0, decimal=12,
                                    err_msg='method %s, function %s' % (name, fname))

        def test_bisect(self):
            self.run_check(bisect, 'bisect')

    test = TestBasic()
    test.test_bisect()
