# -*- coding: utf-8 -*-
"""

Blend two parametric curves.


Created on Thu Sep  8 16:54:25 2016

@author: rarossi
"""
from numpy import sin, cos, linspace, array
from matplotlib import pyplot as plt


def k1(t):
    """First parametric curve.
    User defined
    """
    return array((sin(t), cos(t)))


def k2(t):
    """Second parametric curve.
    User defined
    """
    return array((t**2+2, 1/(t+1)))


def b(t):
    """Parametric blended curve between k1 and k2.
    At t=0, b(0) = k1(0)
    At t=1, b(1) = k2(1)
    Generally: b(t) = k1(t) + t * (k2(t) - k1(t))
    """
    return k1(t) + t * (k2(t) - k1(t))


t = linspace(0, 1, 100)

x1, y1 = k1(t)
x2, y2 = k2(t)
xb, yb = b(t)

plt.plot(x1, y1, 'k',
         x2, y2, 'k',
         xb, yb, 'r')

t = linspace(0, 1, 11)
for to in t:
    plt.plot(*k1(t), 'ok',
             *k2(t), 'ok',
             *b(t), 'or')

x1, y1 = k1(0.5)
x2, y2 = k2(0.5)
plt.plot([x1, x2], [y1, y2], 'k')
