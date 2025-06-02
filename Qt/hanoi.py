# -*- coding: utf-8 -*-
"""

Created on Jul 28 2021

@author: rarossi

"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QColor
import time

STACK, SRC, TMP, DST = [], [], [], []

def hanoi(n, src, dst, tmp):
    '''Recursive Hanoi algorithm. 
    
    src, dst, tmp are lists, for example, in the start of a n == 3 problem,
    the source tower will be src == [3, 2, 1].
    '''
    
    if n > 0:
        hanoi(n-1, src, tmp, dst)
        dst.append(src.pop())
        STACK.append([SRC.copy(), TMP.copy(), DST.copy()])
        hanoi(n-1, tmp, dst, src)


class WorkThread(QtCore.QThread):

    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
        self.animate = False
        self.step = 0
        self.timer = 0.5

    def run(self):
        while True:

            if not self.animate:
                continue
            
            if self.step < len(STACK) - 1:
                self.step += 1
                self.parent.pins = STACK[self.step]
            else:
                self.animate = False
            
            self.parent.update()
            time.sleep(self.timer)

        return


class Window(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.game = WorkThread(self)
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        
        self.animate_btn = QtWidgets.QPushButton('Animate')
        self.reset_btn = QtWidgets.QPushButton('Reset')
        self.plus_btn = QtWidgets.QPushButton('+')
        self.minus_btn = QtWidgets.QPushButton('-')
        
        self.animate_btn.clicked.connect(self.animate)
        self.reset_btn.clicked.connect(self.reset)
        self.plus_btn.clicked.connect(self.increase)
        self.minus_btn.clicked.connect(self.decrease)
        
        self.speed = QtWidgets.QSlider()
        self.speed.setValue(50)
        self.speed.setMaximum(100)
        self.speed.setOrientation(QtCore.Qt.Horizontal)
        self.speed.valueChanged.connect(self.speed_changed)
        
        grid.addWidget(self.animate_btn, 0, 1)
        grid.addWidget(self.reset_btn, 0, 2)
        grid.addWidget(self.plus_btn, 0, 3)
        grid.addWidget(self.minus_btn, 0, 4)
        grid.addWidget(self.speed, 1, 1, 1, 4)
        grid.addItem(QtWidgets.QSpacerItem(500, 500), 2, 0)
        
        self.setWindowTitle('Tower of Hanoi')
        self.setFixedSize(640, 480)
        
        self.pin_selected = 0

        self.N = 3
        self.solve()
        self.game.start()
        self.reset()
        
        self.show()

    def solve(self):
        global STACK, SRC, TMP, DST
        TMP, DST = [], []
        SRC = [self.N-i for i in range(self.N)]
        STACK = [[SRC.copy(), TMP.copy(), DST.copy()]]
        hanoi(self.N, SRC, DST, TMP)
        
    def increase(self):
        if self.N < 10:
            self.N += 1
            self.solve()
            self.reset()
        
    def decrease(self):
        if self.N > 3:
            self.N -= 1
            self.solve()
            self.reset()
            
    def reset(self):
        self.game.animate = False
        self.game.step = 0
        self.solve()
        self.pins = STACK[0]
        self.update()
    
    def speed_changed(self):
        self.game.timer = self.speed.value() / 100
        self.update()
        
    def animate(self):
        self.game.animate = True

    def mousePressEvent(self, event):
        pin_clicked = 0

        if event.y() > 250:
            pin_clicked = 1 if event.x() < 215 else (2 if event.x() < 425 else 3)

        if pin_clicked == 0:
            return

        if self.pin_selected == 0:
            # no previous selection, select the pin
            self.pin_selected = pin_clicked
        else:
            # source pin selected, now select destination pin
            if self.pin_selected == pin_clicked:
                # deselect the pin
                self.pin_selected = 0
            else:
                # move disk from src to dst
                src_pin = self.pin_selected - 1
                dst_pin = pin_clicked - 1
                
                if self.pins[src_pin] and (not self.pins[dst_pin] or self.pins[src_pin][-1] < self.pins[dst_pin][-1]):
                    disk = self.pins[src_pin].pop()
                    self.pins[dst_pin].append(disk)
                
                # reset selection
                self.pin_selected = 0
            
        self.update()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.pin_selected = 0
            self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        qp.setPen(QtCore.Qt.black)

        # background
        qp.fillRect(0, 0, 640, 480, QtCore.Qt.white)
        
        ground = 400
        pin_h = 150
        
        # ground
        qp.fillRect(0, ground, 640, 480 - ground, QtCore.Qt.gray)

        # draw the pins
        pos = [110, 320, 530]
        wt2 = [5, 5, 5]
        wt2[self.pin_selected - 1] = 10 if self.pin_selected else 5
        for x, wt in zip(pos, wt2):
            qp.fillRect(x - wt, ground - pin_h, 2 * wt, pin_h, QtCore.Qt.black)
            
        # draw disks
        diams = [50 + i * 150 // self.N for i in range(self.N)]
        colors = [
            QColor('maroon'),  # largest disk
            QColor('red'),
            QColor('purple'),
            QColor('fuchsia'),
            QColor('green'),
            QColor('lime'),
            QColor('olive'),
            QColor('yellow'),
            QColor('navy'),
            QColor('teal'),  # smallest disk
        ]
        
        for x, pin in zip(pos, self.pins):
            for i, disk in enumerate(pin):
                diam = diams[disk-1]
                qp.fillRect(x - diam//2, ground - 10 * (i+1), diam, 10, colors[len(colors) - disk])
                qp.drawRect(x - diam//2, ground - 10 * (i+1), diam, 10)
        
        qp.drawText(10, 20, f'Disks: {self.N}')
        qp.drawText(10, 35, f'Iteractions: {2**self.N-1}')
        qp.drawText(10, 50, f'Step: {self.game.step}')
        qp.drawText(10, 65, f'Delay: {self.game.timer} s')
        
            
if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
