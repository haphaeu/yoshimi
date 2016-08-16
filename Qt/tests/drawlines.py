#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

In the example, we draw randomly 1000 red points
on the window.

author: Jan Bodnar
website: zetcode.com
last edited: September 2011
"""

import sys, random
from PyQt4 import QtGui, QtCore
import numpy as np


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Points')
        self.show()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):

        qp.setPen(QtCore.Qt.red)
        size = self.size()

        sz=1000
        xo, yo = 0, size.height()/2
        for i in range(sz):
            xf = i/sz * size.width()
            yf = size.height()/2 * np.sin(xf/50) + size.height()/2
            qp.drawLine(xo, yo, xf, yf)
            xo, yo = xf, yf


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()