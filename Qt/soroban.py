# -*- coding: utf-8 -*-
"""

Created on Jul 28 2021

@author: rarossi

"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtTest

import copy
import time


class Window(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        self.mousePressEvent = self.mouse_clicked
        
        self.setWindowTitle('Soroban')
        self.setMinimumSize(700, 270)
        
        self.num_cols = 17 # number of columns/digits
        self.target_aspect = 4 # target board aspect ratio
        self.bx = 20 # border x
        self.by = 40 # border y
        
        self.bead1_gap_at = self.num_cols * [0]
        self.bead5_gap_at = self.num_cols * [1]
        
        #self.dot_at = 0 # zero to represent integers, larger to do floats

        self.show_value = True
        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        
        self.w = self.size().width()  # window width
        self.h = self.size().height() # window height
        
        # board size, lx x ly
        if self.w / self.h > self.target_aspect:
            self.ly = self.h - 2 * self.by
            self.lx = self.target_aspect * self.ly
        else:
            self.lx = self.w - 2 * self.bx
            self.ly = self.lx // self.target_aspect

        self.cx = self.lx // self.num_cols
        self.cy = self.ly // 7
        
        self.ox = (self.w - self.lx - 2 * self.bx) // 2  # x offset
        self.oy = (self.h - self.ly - 2 * self.by) // 2 # y offset
        
    def mouse_clicked(self, event):
        x = event.pos().x()
        y = event.pos().y()
        row = (y - self.oy - self.by) // self.cy
        col = (x - self.ox - self.bx) // self.cx
        #print(f'row, col = {row}, {col}')
        self.move(row, col)

    def move(self, row, col):
        if (0 <= row < 7 and 0 <= col < self.num_cols):
            if row < 2:
                self.bead5_gap_at[col] = row
            else:
                self.bead1_gap_at[col] = row - 2
        self.update()
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_R:
            self.bead5_gap_at = self.num_cols * [1]
            self.bead1_gap_at = self.num_cols * [0]
        elif e.key() == QtCore.Qt.Key_V:
            self.show_value = not self.show_value
        self.update()

    def str_value(self):
        strval = ''
        for e, (p5, p1) in enumerate(zip(self.bead5_gap_at, self.bead1_gap_at)):
            p5 = 1 - p5
            strval += '%d' % (p1 + 5 * p5)
        return strval

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):

        pen = qp.pen()
        
        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtCore.Qt.darkRed)

        w = self.w
        h = self.h
        cx = self.cx
        cy = self.cy
        lx = self.lx
        ly = self.ly
        bx, by = self.bx, self.by
        ox, oy = self.ox, self.oy
        
        # background
        qp.fillRect(0, 0, w, h, QtCore.Qt.white)
        
        # draw the board borders
        pen.setWidth(8)
        qp.setPen(pen)
        qp.drawLine(bx + ox, by + oy, bx + ox + lx, by + oy)
        qp.drawLine(bx + ox + lx, by + oy, bx + ox + lx, by + oy + ly)
        qp.drawLine(bx + ox + lx, by + oy + ly, bx + ox, by + oy + ly)
        qp.drawLine(bx + ox, by + oy + ly, bx + ox, by + oy)
        qp.drawLine(bx + ox, by + oy + 2 * cy, bx + ox + lx, by + oy + 2 * cy)

        # rods (vertical, along y) and ref dots
        pen.setWidth(1)
        qp.setPen(pen)
        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtCore.Qt.gray)
        ex = cx // 2
        for i in range(self.num_cols):
            qp.drawLine(ox + bx + i * cx + ex, oy + by, ox + bx + i * cx + ex, oy + by + ly)
            if (i + 1) % 3 == 0:
                # draw some ref dots
                qp.drawEllipse(ox + bx + i * cx + ex - 3, by + oy + 2 * cy - 3, 6, 6)

        # draw the beads
        sx = 3 * cx // 4
        sy = 3 * cy // 4
        ex = (cx - sx) // 2
        ey = (cy - sy) // 2
        for ix in range(self.num_cols):
            x = ox + bx + ix * cx + ex
            # 5-valued bead
            y = oy + by + ey + cy * (1 if self.bead5_gap_at[ix] == 0 else 0)
            if ix in (0, 1, 5, 6, 7, 11, 12, 13):
                qp.setBrush(QtCore.Qt.darkRed)
            else:
                qp.setBrush(QtCore.Qt.darkYellow)
            qp.drawEllipse(x, y, sx, sy)
            # 1-valued beads
            ibead = 0
            for iy in range(5):
                if iy == self.bead1_gap_at[ix]:
                    continue
                y = oy + by + (iy + 2) * cy + ey
                qp.drawEllipse(x, y, sx, sy)
                ibead += 1

        if self.show_value:
            qp.drawText(10, 10, self.str_value())
        #qp.drawText(10, 35, f'Iteractions: {2**self.N-1}')
        #qp.drawText(10, 50, f'Step: {self.game.step}')
        #qp.drawText(10, 65, f'Delay: {self.game.timer} s')
        
            
if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
