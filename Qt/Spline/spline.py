# -*- coding: utf-8 -*-
"""

Draw a spline from user selected points with the mouse.
Ctrl+E to clear screen.

Created on Tue Aug 16 15:44:46 2016

@author: rarossi

"""

from PyQt4 import QtGui, QtCore
import numpy as np
import scipy.interpolate as itp


class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.points = []
        self.splx, self.sply = [], []

    def mousePressEvent(self, event):
        pt = event.pos()
        self.points.append((int(pt.x()), int(pt.y())))
        if len(self.points) > 3:
            self.calc_spline()

        self.update()
        QtCore.QCoreApplication.processEvents()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        qp.setPen(QtCore.Qt.gray)
        for i in range(len(self.points)):
            qp.drawPoint(self.points[i][0], self.points[i][1])

        for i in range(len(self.points)-1):
            qp.drawLine(self.points[i][0], self.points[i][1],
                        self.points[i+1][0], self.points[i+1][1])

        qp.setPen(QtCore.Qt.red)
        for i in range(len(self.splx)-1):
            qp.drawLine(self.splx[i], self.sply[i],
                        self.splx[i+1], self.sply[i+1])

    def calc_spline(self):
        pts = np.array(self.points)
        x = pts[:, 0]
        y = pts[:, 1]
        # Fits a parametric spline for both x and y
        t = np.linspace(0, 1, len(x))
        tckx = itp.splrep(t, x, per=False)
        tcky = itp.splrep(t, y, per=False)
        ts = np.linspace(0, 1, 1000)
        self.splx = itp.splev(ts, tckx)
        self.sply = itp.splev(ts, tcky)

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            if e.key() == QtCore.Qt.Key_E:  # copy
                self.points = []
                self.splx, self.sply = [], []
                self.update()
                QtCore.QCoreApplication.processEvents()


if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
