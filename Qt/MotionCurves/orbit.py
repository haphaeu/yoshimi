# -*- coding: utf-8 -*-
"""
Ctrl+E to clear screen.
Created on Tue Aug 16 15:44:46 2016
@author: rarossi
"""

from PyQt4 import QtGui, QtCore
import numpy as np
import scipy.interpolate as itp
from math import sin, cos
from matplotlib import pyplot as plt
from time import sleep


class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # make sure mouse motion is captured by mouseMoveEvent
        # otherwise only drag is captured
        self.setMouseTracking(True)
        self.earth_orbit = []
        self.scaled_earth_orbit = []
        self.sun_pos = np.array((0, 0))
        self.scaled_sun_pos = 0
        self.r_earth = 6378.137e3  # m
        self.r_sun = 695700e3  # m
        self.scaled_r_earth = 0
        self.scaled_r_sun = 0

        self.get_earth_orbit()
        self.scale_things()

    def resizeEvent(self, ev):
        print('resize')
        self.scale_things()
        #self.update()
        QtGui.QWidget.resizeEvent(self, ev)

    def mousePressEvent(self, event):
        pt = event.pos()

        self.update()
        QtCore.QCoreApplication.processEvents()

    def mouseMoveEvent(self, ev):
        pt = ev.pos()
        for p in self.earth_orbit:
            if max(abs(p[0] - pt.x()), abs(p[1] - pt.y())) < 10:
                self.hit = p
                break
        else:
            self.hit = False

        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        if len(self.scaled_earth_orbit) > 0:
            qp.setPen(QtCore.Qt.red)
            for i in range(len(self.scaled_earth_orbit)-1):
                qp.drawLine(self.scaled_earth_orbit[i][0], self.scaled_earth_orbit[i][1],
                            self.scaled_earth_orbit[i+1][0], self.scaled_earth_orbit[i+1][1])
            # draw the sun
            qp.drawEllipse(*self.scaled_sun_pos, 2*self.scaled_r_sun, 2*self.scaled_r_sun)

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_E:  # copy
                self.points = []
                self.splx, self.sply = [], []
                self.update()
                QtCore.QCoreApplication.processEvents()

    def get_earth_orbit(self, year_resolution=365):
        """Solver Earth's orbit motion using classic Newton mechanics.
        The Earth is subject to an acceleration pointing towards the sun.
        The initial conditions, the Earth is put at the Aphelion with
        maximum orbital speed.

        https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
        https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
        """

        # Constants
        G = 6.674e-11  # N*(m/kg)^2
        m_earth = 5.9723e24  # kg
        m_sun = 1988500e24  # kg
        aphelion = 147.09e9  # m
        max_orbital_speed = 30.29e3 # m/s

        # earth starts at the aphelion
        # sun is at (0, 0)
        pos_earth = np.array((-aphelion, 0))  # m
        vel_earth = np.array((0, max_orbital_speed))  # m/s

        dt = 365.256*24*3600/(year_resolution-1)  # s
        t = 0  # s

        self.earth_orbit = np.zeros((year_resolution, 2))
        self.earth_orbit[0] = pos_earth

        for i in range(1, year_resolution):
            t += dt
            r = pos_earth.dot(pos_earth)**0.5  # distance earth-sun
            u = -pos_earth/r  # unit vector pointing towards the sun
            force = G * m_earth * m_sun / r**2 * u
            accel = force / m_earth
            vel_earth += accel*dt
            pos_earth += vel_earth*dt
            self.earth_orbit[i] = pos_earth

        with open('orbit.txt', 'w') as pf:
            pf.write(np.array2string(self.earth_orbit))

    def scale_things(self):
        pad = np.array((10, 10))
        canvas_size = np.array([self.size().width(), self.size().height()]) - 2*pad
        shift = pad + canvas_size/2
        orbit_range = self.earth_orbit.max(axis=0) - self.earth_orbit.min(axis=0)
        scale = max(orbit_range / canvas_size)

        self.scaled_earth_orbit = self.earth_orbit / scale + shift
        self.scaled_r_sun = self.r_sun / scale
        self.scaled_r_earth = self.r_earth / scale
        self.scaled_sun_pos = self.sun_pos / scale + shift

        print('canvas_size', canvas_size)
        print('orbit_range', orbit_range)
        print('scale', scale)

# Deprecated
#def kepler(M, e, tol=1e-4, max_iters=100, verbose=False, out_stats=False):
#    """Solves Kepler's Equation.
#
#    M: mean anomaly
#    e: eccentricity
#
#    Return:
#
#    E: eccentric anomaly
#
#    https://en.wikipedia.org/wiki/Kepler%27s_equation
#    """
#    E = M
#    err = 9.9
#    i = 0
#    if verbose:
#        print('iter\t        E\t        err')
#    while abs(err) > tol and i < max_iters:
#        # Newton method to solve trancendental equation
#        err = E-e*sin(E)-M / (1 - e*cos(E))
#        E -= err
#        i += 1
#        if verbose:
#            print('%02d\t%.8f\t%.8f' % (i, E, err))
#    if out_stats:
#        return E, err, i
#    else:
#        return E



if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
