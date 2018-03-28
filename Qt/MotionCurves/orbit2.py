# -*- coding: utf-8 -*-
"""

Draws Earth orbiting around the Sun.

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

        # Constants
        self.G = 6.674e-11  # N*(m/kg)^2
        self.m_earth = 5.9723e24  # kg
        self.m_sun = 1988500e24  # kg
        self.aphelion = 147.09e9  # m
        self.max_orbital_speed = 30.29e3 # m/s

        # earth starts at the aphelion
        # sun is at (0, 0)
        self.pos_earth = np.array((-self.aphelion, 0))  # m
        self.vel_earth = np.array((0, self.max_orbital_speed))  # m/s

        self.dt = 24*3600  # s
        self.t = 0

        # make sure mouse motion is captured by mouseMoveEvent
        # otherwise only drag is captured
        self.setMouseTracking(True)
        self.sun_pos = np.array((0, 0))
        self.scaled_sun_pos = (0, 0)
        self.r_earth = 6378.137e3  # m
        self.r_sun = 695700e3  # m
        self.fdraw_earth = 400
        self.fdraw_sun = 50

        self.scaled_earth_orbit = []
        self.scaled_earth_pos = []
        self.scaled_r_earth = 0
        self.scaled_r_sun = 0
        self.draw_orbit = False

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.loop)
        self.timer.start(10)

    def resizeEvent(self, ev):
        print('resize')
        self.scale_things()
        QtGui.QWidget.resizeEvent(self, ev)

#    def mousePressEvent(self, event):
#        pt = event.pos()
#        self.update()
#        QtCore.QCoreApplication.processEvents()

#    def mouseMoveEvent(self, ev):
#        pt = ev.pos()
#        for p in self.earth_orbit:
#            if max(abs(p[0] - pt.x()), abs(p[1] - pt.y())) < 10:
#                self.hit = p
#                break
#        else:
#            self.hit = False
#        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        qp.setPen(QtCore.Qt.red)
        box = self.fdraw_sun * 2 * self.scaled_r_sun
        qp.drawEllipse(*self.scaled_sun_pos, box, box)
        box = self.fdraw_earth * 2 * self.scaled_r_earth
        qp.drawEllipse(*self.scaled_earth_pos, box, box)
        if self.draw_orbit:
            for i in range(len(self.scaled_earth_orbit)-1):
                qp.drawLine(self.scaled_earth_orbit[i][0], self.scaled_earth_orbit[i][1],
                            self.scaled_earth_orbit[i+1][0], self.scaled_earth_orbit[i+1][1], )

    def keyPressEvent(self, e):
        #
        # W: increase earth's orbital speed
        # S: decrease earth's orbital speed
        # O: draw past orbit
        # E: erase orbit
        if e.key() == QtCore.Qt.Key_W:
            print('Pressed W')
            self.vel_earth *= 1.1
        if e.key() == QtCore.Qt.Key_S:
            print('Pressed S')
            self.vel_earth /= 1.1
        if e.key() == QtCore.Qt.Key_O:
            print('Pressed O')
            self.draw_orbit = not self.draw_orbit
        if e.key() == QtCore.Qt.Key_E:
            print('Pressed E')
            self.scaled_earth_orbit = []
        QtCore.QCoreApplication.processEvents()


    def loop(self):
        self.update_orbit()
        self.update()


    def update_orbit(self):
        """Solver Earth's orbit motion using classic Newton mechanics.
        The Earth is subject to an acceleration pointing towards the sun.
        The initial conditions, the Earth is put at the Aphelion with
        maximum orbital speed.

        https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
        https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
        """

        self.t += self.dt
        r = self.pos_earth.dot(self.pos_earth)**0.5  # distance earth-sun
        u = -self.pos_earth/r  # unit vector pointing towards the sun
        force = self.G * self.m_earth * self.m_sun / r**2 * u
        accel = force / self.m_earth
        self.vel_earth += accel*self.dt
        self.pos_earth += self.vel_earth*self.dt

        self.scaled_earth_pos = self.pos_earth / self.scale + self.shift

        self.scaled_earth_orbit.append(self.scaled_earth_pos)

    def scale_things(self):
        print('re-scaling')
        pad = np.array((10, 10))
        canvas_size = np.array([self.size().width(), self.size().height()]) - 2*pad
        self.shift = pad + canvas_size/2
        # orbit_range = self.earth_orbit.max(axis=0) - self.earth_orbit.min(axis=0)
        orbit_range = 2.99258415e+11
        self.scale = max(orbit_range / canvas_size)

        # not here
        # self.scaled_earth_pos = self.pos_earth / scale + shift
        # self.scaled_earth_orbit = self.earth_orbit / scale + shift
        self.scaled_r_sun = self.r_sun / self.scale
        self.scaled_r_earth = self.r_earth / self.scale
        self.scaled_sun_pos = self.sun_pos / self.scale + self.shift
        self.scaled_earth_pos = self.pos_earth / self.scale + self.shift
        self.scaled_earth_orbit = [self.scaled_earth_pos]


# # Deprecated
# def kepler(M, e, tol=1e-4, max_iters=100, verbose=False, out_stats=False):
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
