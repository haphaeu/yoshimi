# -*- coding: utf-8 -*-
"""

Solvers for catenary equation, including a 2-weight-segments catenary solver.


Created on Tue Apr  3 13:32:55 2018

@author: rarossi
"""
import time
import numpy
import scipy.optimize
from matplotlib import pyplot as plt
from numpy import sinh, cosh, sqrt, log, arcsinh


def ycat(a, x):
    return a * cosh(x / a)


def solve_catenary_parameter(h, d, s, tol=1e-6, max_iter=100, a0=False, verbose=False):
    """Solved the parameter 'a' of the catenary equation:

        y(x) = a.cosh(x/a)

    Given vertical and horizontal difference between end points and
    the length. Written with those terms, the catenary equation
    becomes [1]:

        2*a*sinh(d/2/a) = sqrt(s**2 - h**2)

    This is solved for a using Newton-Raphson method by using:

        f(a) = 2*a*sinh(d/2/a) - sqrt(s**2 - h**2)

        df(a)/da = 2*sinh(d/2/a) - d/a*cosh(d/2/a)

    Note that given the nature of these functions, a good choice for the
    starting point for a is very important.

    Arguments:

        h: height difference between ends
        d: distance horizontal between ends
        s: length of catenary

    Optional arguments:

        tol: solver tolerance
        max_iter: maximum solver iterations
        a: initial guess for catenary parameter
        verbose: output solver iterations

    [1] http://mathhelpforum.com/calculus/96398-catenary-cable-different-heights.html#post343702

    """
    assert s > sqrt(h**2 + d**2), 'Length too short.'

    # If a0 is not given (set to False), calculate a rough estimate of a
    # starting point using an empirical value.
    a0 = a0 if a0 else 10
    a = a0

    if verbose:
        print('solve_catenary_parameter')
        print('h, d, s, ao:', h, d, s, a)
        print('i a fa dfa')
    for i in range(max_iter):
        fa = 2*a*sinh(d/2/a) - sqrt(s**2 - h**2)
        dfa = 2*sinh(d/2/a) - d/a*cosh(d/2/a)
        a = a - fa/dfa
        if verbose: print(i, a, fa, dfa)

        # If the starting point for a is not good enough, the solver will
        # diverge into negative values for a or f(a).
        # In these cases, correct the starting point by making it smaller and
        # restart.
        if (a < 0) or (fa < 0):
            a0 /= 1.1
            a = a0
            if verbose: print('Corrected a to', a)
        if abs(fa) < tol:
            break
    else:
        print('Reached max_iter - current error is ', fa)

    return a


def max_depth(h, d, s, a=False):
    if not a:
        a = solve_catenary_parameter(h, d, s)
    x1, x2 = domain(h, d, s, a)
    y1 = ycat(a, x1)
    y2 = ycat(a, x2)
    return max(y1, y2) - a


def domain(h, d, s, a=False):
    if not a:
        a = solve_catenary_parameter(h, d, s)
    x1 = 0.5 * (a*log((s+h)/(s-h)) - d)
    x2 = 0.5 * (a*log((s+h)/(s-h)) + d)
    return x1, x2


def arc_length(a, x):
    """Arc length along the catenary at coordinate x.

    Note that arc_length(a, 0) = 0
    """
    return a * sinh(x/a)


def x_from_arc_length(a, s):
    """X coordinate corresponding to an arc length.

    Note that x_from_arc_length(a, 0) = 0
    """
    return a * arcsinh(s/a)


def calc_end_reactions(h, d, s, w, a=False):
    if not a:
        a = solve_catenary_parameter(h, d, s)
    x1, x2 = domain(h, d, s, a)
    return calc_reaction(a, x1, w), calc_reaction(a, x2, w, side='right')


def calc_reaction(a, x, w, side='left', verbose=False):
    """Calculate the reaction tension vector at the catenary cable.

    calc_reaction(a, x, w) ==> (Fh, Fv)

    Arguments:

        a: catenary parameter.

        x: x-coordinate to calculate reaction at.

        w: unit weight of the cable

        side: 'left' or 'right'. Indicate what side of the point to
              calculate the reaction for. 'left' means that the reaction
              is calculated at the left side of the point x.
    """
    side = side.lower()
    assert side in ('left', 'right')

    # assume left side
    Rh = a*w
    Rv = w*a*sinh(x/a)
    # invert sign in case of right side
    if side == 'right':
        Rh *= -1
        Rv *= -1

    if verbose:
        R = sqrt(Rv**2 + Rh**2)
        print('a, x, w:', a, x, w)
        print('Rv:', Rv)
        print('Rh:', Rh)
        print('R:', R)

    return (Rh, Rv)


def test_calc_reaction():
    h, d, s = 0, 50, 200
    a = solve_catenary_parameter(h, d, s)
    x1, x2 = domain(h, d, s, a)
    s1, s2 = arc_length(a, (x1, x2))
    x = numpy.linspace(s1, s2, 100)
    w = 2
    y = [calc_reaction(a, x_from_arc_length(a, xi), w) for xi in x]
    y = [sqrt(yi[0]**2 + yi[1]**2) for yi in y]
    plt.plot(x, y)


def solve_multi_segment():
    """Solves a catenary with 2 segments of different weights.
    """

    # segments lengths
    s1, s2 = 50, 80
    # weights
    w1, w2 = 4, 1
    # ends difference
    h, d = -10, 80

    def func(x0):
        """Returns the magnitude of the reaction force at the transition
        node between 2 catenaries. This reaction force must be zero is the
        configuration converges.

        This is used in a scipy.optimize.minimize() algorithm to find the
        catenary configuration.

        The input x = numpy.array([h1, d1]), which are the vertical height and
        horizontal distance between both ends _for the first catenary_. The
        values h1, d2 for the seconds canetary are calculated based on the
        target configuration.
        """
        h1, d1 = x0
        h2, d2 = h-h1, d-d1

        # If (h1, d1) is out of range for s1, return a high value so that
        # this pair is not considered a good solution.
        if (s1 < sqrt(h1**2 + d1**2)) or (s2 < sqrt(h2**2 + d2**2)):
            return 9999.99

        a1 = solve_catenary_parameter(h1, d1, s1)
        a2 = solve_catenary_parameter(h2, d2, s2)
        if numpy.any(numpy.isnan((a1, a2))):
            print('Got nan - break')
            print('a1, a2', a1, a2)
            print('h1, d1, s1:', h1, d1, s1)
            raise SystemExit
        x11, x12 = domain(h1, d1, s1, a1)
        x21, x22 = domain(h2, d2, s2, a2)
        R1 = numpy.array(calc_reaction(a1, x12, w1, 'right'))
        R2 = numpy.array(calc_reaction(a2, x21, w2, 'left'))
        R = R1+R2

        if False:
            print('='*40)
            plt.plot(*get_points(a1, x11, x12, shiftX=-x12, shiftY=ycat(a2, x21)-ycat(a1, x12)))
            plt.plot(*get_points(a2, x21, x22, shiftX=-x21, shiftY=0))
            plt.show()
            print('h1, d1', h1, d1)
            print('h2, d2', h2, d2)
            print('a:', a1, a2)
            print('R1', R1)
            print('R2', R2)
            print('Unballanced force', R)

        return sqrt(R[0]**2 + R[1]**2)

    #  The starting point for the solver is the uniform weight catenary
    #
    # Catenary parameters for a uniform weight catenary
    a_eq = solve_catenary_parameter(h, d, s1+s2)
    x_eq = domain(h, d, s1+s2, a_eq)
    s1_eq = arc_length(a_eq, x_eq[0])
    # d1o is the distance along the x axis from the left end of the catenary
    # until the point where the uniform catenary arc length equals to s1.
    # h1o is analogous to d1o, but in terms of height difference
    # (h1o, d1o) is the starting point for the solver.
    d1o = x_from_arc_length(a_eq, s1_eq+s1) - x_eq[0]
    h1o = ycat(a_eq, x_eq[0]+d1o) - ycat(a_eq, x_eq[0])

    tr = time.time()
    ret = scipy.optimize.minimize(func, numpy.array((h1o, d1o)),
                                  method='TNC',  # bounds=((-min(s1, s2), 0), (0, d)),
                                  options={'maxiter': 1000, 'ftol': 1e-6})
    tr = time.time() - tr

    print('='*40)
    print('Minimize runtime %.2fs.' % tr)
    print('R:', ret.fun)
    print(ret.message)
    h1, d1 = ret.x
    h2, d2 = h-h1, d-d1
    plot_catenaries(h1, d1, s1, w1, h2, d2, s2, w2)


def plot_catenaries(h1, d1, s1, w1, h2, d2, s2, w2):
    a1 = solve_catenary_parameter(h1, d1, s1)
    a2 = solve_catenary_parameter(h2, d2, s2)
    x11, x12 = domain(h1, d1, s1, a1)
    x21, x22 = domain(h2, d2, s2, a2)
    figsize = (6, 5)

    cat1 = get_points(a1, x11, x12, shiftX=-x11, shiftY=-ycat(a1, x11),
                      save=True, mode='w')
    cat2 = get_points(a2, x21, x22, shiftX=x12-x11-x21,
                      shiftY=-ycat(a1, x11)-ycat(a2, x21)+ycat(a1, x12),
                      save=True, mode='a')

    # Plots limits based on points
    x_lims = [min(min(cat1[0]), min(cat2[0])), max(max(cat1[0]), max(cat2[0]))]
    y_lims = [min(min(cat1[1]), min(cat2[1])), max(max(cat1[1]), max(cat2[1]))]
    x_range = x_lims[1] - x_lims[0]
    y_range = y_lims[1] - y_lims[0]

    # Aspect ratio
    plot_aspect_ratio = x_range / y_range
    canvas_aspect_ratio = figsize[0] / figsize[1]

    if plot_aspect_ratio > canvas_aspect_ratio:
        y_factor = plot_aspect_ratio/canvas_aspect_ratio
        y_ave = (y_lims[0]+y_lims[1])/2
        y_lims = [y_ave-y_range*y_factor/2, y_ave+y_range*y_factor/2]
    else:
        x_factor = canvas_aspect_ratio/plot_aspect_ratio
        x_ave = (x_lims[0]+x_lims[1])/2
        x_lims = [x_ave-x_range*x_factor/2, x_ave+x_range*x_factor/2]

    plt.figure(figsize=figsize)
    plt.plot(*cat1, lw=w1)
    plt.plot(*cat2, lw=w2)
    plt.xlim(x_lims)
    plt.ylim(y_lims)
    plt.grid()


def get_points(a, x1, x2, pts=100, shiftX=0, shiftY=0, save=False, mode='w'):
    delta = (x2-x1)/(pts-1)
    x, y = [0]*pts, [0]*pts
    buffer = ''
    for i in range(pts):
        x[i] = x1 + i*delta + shiftX
        y[i] = ycat(a, x[i] - shiftX) + shiftY
        buffer += '%.3f \t %.3f \n' % (x[i], y[i])
    if save:
        with open('points.txt', mode) as pf:
            pf.write(buffer)
    return x, y


def unit_test():
    if (solve_catenary_parameter(250, 400, 700) - 111.10765390219983) < 1e-6:
        return True
    return False


if __name__ == '__main__':
    # calc_catenary(250, 400, 700)
    solve_multi_segment()
