# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 15:44:46 2016

@author: rarossi

source:
http://stackoverflow.com/a/13370267/5069105
"""

from PyQt4 import QtGui, QtCore


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

    def mousePressEvent(self, event):
        if self.points == 2:
            self.scene().clear()
            self.points = 0

        self._start = event.pos()
        start = QtCore.QPointF(self.mapToScene(self._start))
        text = self.scene().addSimpleText('(%d, %d)' % (start.x(), start.y()))
        text.setBrush(QtCore.Qt.red)
        text.setPos(start)
        self.points += 1

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
