# -*- coding: utf-8 -*-
"""

Time to drain the water from a horizontal pipe through an orifice at the bottom.

Jet speed is v = sqrt(2gh), being h the height of water inside the pipe.

chord = diam * sqrt(1 - ((h - r)/r)**2)

Created on Tue May 19 15:46:53 2015

@author: rarossi

"""
from math import sin, asin, pi
from matplotlib import pyplot as plt
from scipy.optimize import bisect
g = 9.806     # m/s^2
_debug = False


def chord(r, d):
    """Return the length of the chord of a circle of radius r at a distance d
    from the centre."""
    return 2 * r * (1 - (d/r)**2)**0.5


def area_above_segment(r, h):
    """radius, height --> area of the circular segment above a chord at height"""
    c = chord(r, abs(h-r))
    theta = 2 * asin(c/2/r)
    area_segment = r**2 / 2 * (theta - sin(theta))
    if h >= r:
        return area_segment
    else:
        return pi*r**2 - area_segment


def calc_dh(area, h0, r):
    if _debug: print(area, h0)

    def func(h):
        return area_above_segment(r, h) - area_above_segment(r, h0) - area

    return h0 - bisect(func, 0, 2*r)


def fill_ratio(r, h):
    """Horizontal pipe of radius r, filled with water at a height h.
    Return the water fill ratio"""
    c = chord(r, h-r)
    theta = 2 * asin(c / (2*r))
    factor = (theta - sin(theta)) / (2*pi)
    return factor if h < r else 1-factor


# geometry
pd = 0.4  # m, pipe diameter
pl = 1.5  # m, pipe length
ao = 0.1 * 0.06 + pi/4 * 0.06**2  # m2, orifice area

# time traces
dt = 1e-2  # s
t = 0.0   # s
h = 0.91 * pd
time, height, fill = [t], [h], [fill_ratio(pd/2, h)]

while h > 1e-3:
    if _debug: print(t)
    t += dt
    area = dt * (2*g*h)**0.5 * ao / pl
    h -= calc_dh(area, h, pd/2)
    time.append(t)
    height.append(h)
    fill.append(fill_ratio(pd/2, h))

plt.plot(time, fill)
plt.title('fill')
plt.xlabel('Time [s]')
plt.ylabel('Fill ratio')
plt.grid()
plt.show()
print('%.1f seconds to empty the pipe' % t)
