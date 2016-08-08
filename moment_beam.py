# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 16:43:45 2016

@author: rarossi
"""

from matplotlib import pyplot as plt
import numpy as np
from pylab import rcParams
rcParams['figure.figsize'] = 10, 5


def moment(x, d=0.207, l=1, w=1, W=0):
    """Returns the bending moment at a point along a symmetrically supported beam with point
    loads at both ends:

            v W [N]                     v W [N]
            [===========================]
                  ^               ^
            |--d--|
            |---------> x

    x [m] is the distance along the beam
    d [m] is the distance from the end of the beam to the support
    l [m] is the total length of the beam
    w [N/m] is the linear weight of the beam
    W [N] is the point load at ends of the beam (flanges)

    Weights can also be input as [kgf], in wich case the moment will be in [kgf.m]
    """
    if d < 0 or d > l/2:
        raise SystemExit
    if x < 0 or x > l:
        return 0.0
    elif x <= d:
        return W*x + w*x**2/2
    elif x <= l-d:
        return W*d + w*d**2/2 - w/2*(x-d)*(l-x-d)
    else:
        return W*(l-x) + w*(l-x)**2/2


def optimal_support(l, w, W):
    """Return the optimal distance, d, of the supports from the end of the beam.
    The bending moment along the beam is minimal for this distance.

    l [m] - length of the beam
    w [N/m] - linear weight of the beam
    W [N] - point load at both ends of the beam

    Weights can also be input as [kgf], in wich case the moment will be in [kgf.m]

    This is the solution of the following equation:

        moment(d) = - moment(l/2)
    """
    return (-(4*W/w+l)+np.sqrt((4*W/w+l)**2+l**2))/2


if __name__ == '__main__':
    W = 750  # kg
    w = 100  # kg/m
    l = 50  # m

    d = optimal_support(l, w, W)

    X = np.linspace(0, l, 100)
    M = np.array([moment(x, d=d, l=l, w=w, W=W) for x in X])
    M1 = np.array([moment(x, d=1.1*d, l=l, w=w, W=W) for x in X])
    M2 = np.array([moment(x, d=0.9*d, l=l, w=w, W=W) for x in X])

    plt.plot(X, M, 'b')
    plt.plot(X, M1, '.k')
    plt.plot(X, M2, '.k')
    plt.grid()
    title = 'Bending moment along beam - Optimised support distance\n'
    title += 'Pipe linear weight %.0f kg/m - Flanges weight %.0f kg' % (w, W)
    plt.title(title)
    plt.xlabel('Distance along beam [m]')
    plt.ylabel('Bending Moment [N.m]')
    plt.show()

    # Plot d(W/w, l)
    L = np.linspace(5, 50, 100)
    w = 1
    for r in range(6):
        W = r*w
        d = [optimal_support(l, w, W) for l in L]
        plt.plot(L, d/L, label='W/w = %d' % r)
    plt.grid()
    plt.legend(loc='best')
    plt.title('Optimimum Support Distance for various W/w ratios')
    plt.xlabel('Beam length [m]')
    plt.ylabel('Support Distance over Beam Length Ratio (d/l)')
