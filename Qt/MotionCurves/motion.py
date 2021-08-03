# -*- coding: utf-8 -*-
"""
Ctrl+E to clear screen.
Created on Tue Aug 16 15:44:46 2016
@author: rarossi
"""

from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
#import scipy.interpolate as itp


class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # make sure mouse motion is captured by mouseMoveEvent
        # otherwise only drag is captured
        self.setMouseTracking(True)
        self.hit = False

        self.points = []

    def mousePressEvent(self, event):
        pt = event.pos()

        # remove existing point if clicked within a threshold
        for p in self.points:
            if max(abs(p[0] - pt.x()), abs(p[1] - pt.y())) < 10:
                self.points.remove((p))
                break
        else:
            self.points.append((int(pt.x()), int(pt.y())))
            # sort to make sure that the x coordinate is in ascending order
            self.points.sort()

        self.update()
        QtCore.QCoreApplication.processEvents()

    def mouseMoveEvent(self, ev):
        pt = ev.pos()
        for p in self.points:
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
        self.drawHit(qp)
        qp.end()

    def drawHit(self, qp):
        if self.hit:
            qp.setPen(QtCore.Qt.blue)
            qp.drawText(QtCore.QPointF(*self.hit), 'delete')

    def drawLines(self, qp):

        qp.setPen(QtCore.Qt.gray)
        for i in range(len(self.points)):
            qp.drawPoint(self.points[i][0], self.points[i][1])

        qp.setPen(QtCore.Qt.red)
        for i in range(len(self.points)-1):
            qp.drawLine(self.points[i][0], self.points[i][1],
                        self.points[i+1][0], self.points[i+1][1])

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_E:  # copy
                self.points = []
                self.splx, self.sply = [], []
                self.update()
                QtCore.QCoreApplication.processEvents()


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
