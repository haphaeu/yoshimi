# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:44:46 2016

@author: rarossi

source:
http://stackoverflow.com/a/13370267/5069105
"""

from PyQt4 import QtGui, QtCore
import pathfinding as pf
from os import path

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.view = View(self)
        self.button = QtGui.QPushButton('Clear View', self)
        self.button.clicked.connect(self.handleClearView)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.button)

    def handleClearView(self):
        self.view.scene().clear()


class View(QtGui.QGraphicsView):
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self.setScene(QtGui.QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        self.points = 0
        self.display_image(_imname)

    def mousePressEvent(self, event):
        self._pt = event.pos()
        point = QtCore.QPointF(self.mapToScene(self._pt))

        if self.points == 0:
            self.scene().clear()
            self.display_image(_imname)
            self.start = point
            self.goal = self.start
            self.points = 1

        elif self.points == 1:
            self.goal = point
            start = (int(self.start.x()), int(self.start.y()))
            goal = (int(self.goal.x()), int(self.goal.y()))
            do_it(start, goal)
            self.display_image(_imname_mp)
            self.points = 0

        # for point in (self.start, self.goal):
        #    text = self.scene().addSimpleText('(%d, %d)' % (point.x(), point.y()))
        #    text.setBrush(QtCore.Qt.red)
        #    text.setPos(point)


    def display_image(self, fname):
        with open(fname, 'rb') as f:
            content = f.read()
        self.image = QtGui.QImage()
        self.image.loadFromData(content)
        w, h = self.image.size().width(), self.image.size().height()
        pixMap = QtGui.QPixmap.fromImage(self.image)
        self.scene().addPixmap(pixMap)
        self.fitInView(QtCore.QRectF(0, 0, 2*w, 2*h), QtCore.Qt.IgnoreAspectRatio)
        self.scene().update()
        QtCore.QCoreApplication.processEvents()


def do_it(start, goal):
    grid = pf.GridFromImage(_imname)
    came_from1, cost_so_far1 = pf.a_star_search(grid, start, goal, verbose=True)
    grid.show_path(start, goal, came_from1, save=True)

_imname = 'plan_low.bmp'
_imname_mp = 'plan_low_minpath.png'

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
