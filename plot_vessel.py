# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 17:05:26 2017

@author: raf
"""

import numpy as np
from matplotlib import pyplot as plt


def vessel(l, b):
    return np.array([(0, b/2), (l, b/2), (1.05*l, 0), (l, -b/2), (0, -b/2), (0, b/2)])


def rig(a):
    return np.array([(a/2, a/2), (a/2, -a/2), (-a/2, -a/2), (-a/2, a/2), (a/2, a/2)])


def rot(pts, phi, origin=(0, 0)):
    """Rotate points by phi around origin."""
    origin = np.asarray(origin)
    c, s = np.cos(np.radians(-phi)), np.sin(np.radians(-phi))
    return shift(np.dot(shift(pts, -origin), np.array(((c, -s), (s, c)))), origin)


def shift(pts, delta):
    """Translate points by delta."""
    return pts + delta


if __name__ == '__main__':

    # ship
    l, b = 150, 30
    origin = np.array((l, 0))
    heading = -250
    pts_v = shift(rot(vessel(l, b), heading, origin), (400, -100))

    # rig
    side = 40
    head = -160
    pts_r = rot(rig(side), head)

    ax = plt.gca()
    ax.cla()
    ax.plot(*pts_r.transpose())
    ax.plot(*pts_v.transpose())
    circle1 = plt.Circle((0, 0), 50, color='k', ls='--', fill=False)
    circle2 = plt.Circle((0, 0), 550, color='k', ls='--', fill=False)
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.set_xlim(-500, 500)
    ax.set_ylim(-500, 500)
    ax.grid()
    ax.axis('equal')
