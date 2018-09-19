# -*- coding: utf-8 -*-
"""

Probe lander on planet's surface.

Control thrust either manually or using a PID controller.

PID controller implementation very basic. All parameters hard coded.

Created on Sep 09 2018

@author: rarossi

"""

from PyQt4 import QtGui, QtCore
from math import radians, sin, cos, exp
import time

import PIDController

g = 10


class WorkThread(QtCore.QThread):

    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent

        self.timer = 0.1
        self.ship = [[0, 0], [10, 0], [10, -10], [5, -15], [0, -10], [0, 0]]
        self.ship_rocket = [(-3, 20), (-2, 20), (3, 20), (2, 20), (-1, 20), (1, 20)]
        self.k = False
        self.mass = 1000
        self.max_thrust = 5 * self.mass * g
        self.thrust = 1.1 * self.mass * g / self.max_thrust * 100
        self.thrust_on = 1
        self.vy = 0
        self.pos = [320, 50]

        self.controller = PIDController.PIDController()
        self.self_controlled = True

        self.game_over = False

    def run(self):
        while True:
            if self.game_over:
                continue
            dt = 0.1

            if self.self_controlled:
                target = 4 if self.pos[1] > 400 else 15
                self.thrust = self.controller.Calculate(self.vy, target, dt)

            if self.pos[1] < 465:
                self.vy += g*dt - self.thrust_on * self.thrust/100 * self.max_thrust / self.mass * dt
                self.pos[1] += self.vy*dt
            else:
                if self.vy > 5:
                    self.vy = 0
                    self.pos[1] = 465
                    self.game_over = True
                elif g*dt < self.thrust_on * self.thrust/100 * self.max_thrust / self.mass * dt:
                    self.vy += g*dt - self.thrust_on * self.thrust/100 * self.max_thrust / self.mass * dt
                    self.pos[1] += self.vy*dt
                else:
                    self.vy = 0
                    self.pos[1] = 465
            self.parent.update()
            time.sleep(self.timer)

        return


class Window(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setFixedSize(640, 480)
        self.game = WorkThread(self)
        self.game.start()

    def mousePressEvent(self, event):
        if self.game.self_controlled:
            return
        self.game.thrust_on = 1
        if self.game.game_over:
            self.game.game_over = False
            self.game.pos[1] = 50

    def mouseReleaseEvent(self, event):
        if self.game.self_controlled:
            return
        self.game.thrust_on = 0

    def wheelEvent(self, event):
        if self.game.self_controlled:
            return
        self.game.thrust = min(100, max(0, self.game.thrust + event.delta()/50))
        self.update()

    def keyPressEvent(self, e):
        # press C to toogle auto pilot
        if e.key() == QtCore.Qt.Key_C:
            self.game.self_controlled = not self.game.self_controlled
            if self.game.self_controlled:
                self.game.thrust_on = True

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        qp.setPen(QtCore.Qt.red)

        # draw the landing platform
        qp.fillRect(0, 465, 640, 480, QtCore.Qt.blue)

        # draw the ship
        for i in range(len(self.game.ship)-1):
            qp.drawLine(self.game.ship[i][0] + self.game.pos[0],
                        self.game.ship[i][1] + self.game.pos[1],
                        self.game.ship[i+1][0] + self.game.pos[0],
                        self.game.ship[i+1][1] + self.game.pos[1])

        # draw the rocket fire
        if self.game.thrust_on:
            self.game.k = not self.game.k
            i = int(self.game.k)
            qp.drawLine(5 + self.game.pos[0],
                        self.game.pos[1],
                        5 + self.game.ship_rocket[0+i][0] + self.game.pos[0],
                        self.game.thrust/100*(self.game.ship_rocket[0+i][1]) + self.game.pos[1])
            qp.drawLine(5 + self.game.pos[0],
                        self.game.pos[1],
                        5 + self.game.ship_rocket[2+i][0] + self.game.pos[0],
                        self.game.thrust/100*(self.game.ship_rocket[2+i][1]) + self.game.pos[1])
            qp.drawLine(5 + self.game.pos[0],
                        self.game.pos[1],
                        5 + self.game.ship_rocket[4+i][0] + self.game.pos[0],
                        self.game.thrust/100*(self.game.ship_rocket[4+i][1]) + self.game.pos[1])

        # draw thrust meter
        qp.drawRect(10, 75, 20, 200)
        h = 1.98 * self.game.thrust
        y = 275 - h
        qp.fillRect(12, y, 17, h, QtCore.Qt.blue)

        # draw speed meter
        # using a sigmoid function to gain sensetivity on low speed range
        qp.drawArc(-50, 75, 200, 200, -1440, 2880)
        theta = radians(min(90, max(-90, 180/(1+exp(-self.game.vy/5))-90)))
        r = 100
        qp.drawLine(50, 175, 50+r*cos(theta), 175+r*sin(theta))
        for v in [-20, -10, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 10, 20]:
            theta = radians(180/(1+exp(-v/5))-90)
            qp.drawText(50+1.1*r*cos(theta), 175+1.1*r*sin(theta), str(v))

        # stats texts
        qp.drawText(10, 10, 'Thrust %d %% - %s' % (self.game.thrust, 'ON' if self.game.thrust_on else 'OFF'))
        qp.drawText(10, 20, 'Speed %.1f' % self.game.vy)
        qp.drawText(10, 30, 'Y %.1f' % self.game.pos[1])
        if self.game.self_controlled:
            qp.drawText(10, 50, 'AUTO PILOT')
        if self.game.game_over:
            qp.drawText(320, 240, 'Game Over')
            time.sleep(1)

            
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    # window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
