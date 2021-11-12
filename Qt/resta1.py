# -*- coding: utf-8 -*-
"""

Created on Jul 28 2021

@author: rarossi

"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QColor
import copy
import time


board0 = [
   # 0  1  2  3  4  5  6
    [9, 9, 1, 1, 1, 9, 9],  # 0
    [9, 9, 1, 1, 1, 9, 9],  # 1
    [1, 1, 1, 1, 1, 1, 1],  # 2
    [1, 1, 1, 0, 1, 1, 1],  # 3
    [1, 1, 1, 1, 1, 1, 1],  # 4
    [9, 9, 1, 1, 1, 9, 9],  # 5
    [9, 9, 1, 1, 1, 9, 9],  # 6  
]

board = copy.deepcopy(board0)

def rc2a1(row, col):
    return '%s%d' % ('ABCDEFG'[col], row + 1)
    
def get_targets(row, col):

    # clicked on an empty cell or outside board -> nothing to do
    if board[row][col] == 0 or board[row][col] == 99:
        return []
    
    # Possible targets
    potential_targets = [
        (row, col - 2),
        (row, col + 2),
        (row - 2, col),
        (row + 2, col),
    ]
    potential_kills = [
        (row, col - 1),
        (row, col + 1),
        (row - 1, col),
        (row + 1, col),
    ]
    possible_targets = []
    for (candidate_row, candidate_col), (kill_row, kill_col) in zip(
            potential_targets, potential_kills
    ):
        if (0 <= candidate_row < 7
            and 0 <= candidate_col < 7
            and board[candidate_row][candidate_col] == 0
            and board[kill_row][kill_col] == 1
        ):
            possible_targets.append((candidate_row, candidate_col))
    return possible_targets

def draw():
    buffer = '   A B C D E G F\n'
    for k, row in enumerate(board):
        buffer += '%d ' % (k + 1)
        for peg in row:
            if peg == 9:
                buffer += '  '
            elif peg == 1:
                buffer += ' 0'
            else:
                buffer += ' .'
        buffer += '\n'
    print(buffer)


class Window(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        self.mousePressEvent = self.mouse_clicked
        
        #self.animate_btn = QtWidgets.QPushButton('Animate')
        #self.reset_btn = QtWidgets.QPushButton('Reset')
        #self.plus_btn = QtWidgets.QPushButton('+')
        #self.minus_btn = QtWidgets.QPushButton('-')
        #
        #self.animate_btn.clicked.connect(self.animate)
        #self.reset_btn.clicked.connect(self.reset)
        #self.plus_btn.clicked.connect(self.increase)
        #self.minus_btn.clicked.connect(self.decrease)
        #
        #self.speed = QtWidgets.QSlider()
        #self.speed.setValue(50)
        #self.speed.setMaximum(100)
        #self.speed.setOrientation(QtCore.Qt.Horizontal)
        #self.speed.valueChanged.connect(self.speed_changed)
        #
        #grid.addWidget(self.animate_btn, 0, 1)
        #grid.addWidget(self.reset_btn, 0, 2)
        #grid.addWidget(self.plus_btn, 0, 3)
        #grid.addWidget(self.minus_btn, 0, 4)
        #grid.addWidget(self.speed, 1, 1, 1, 4)
        #grid.addItem(QtWidgets.QSpacerItem(500, 500), 2, 0)
        
        self.setWindowTitle('Resta Um')
        self.setFixedSize(490, 490)

        # Help vars used for selection of multiple targets
        self.targets = []
        self.origin = 0, 0
        
        self.show()

    def mouse_clicked(self, event):
        x = event.pos().x()
        y = event.pos().y()
        row = y // 70
        col = x // 70

        if not self.targets == []:
            # Selecting from multiple targets
            targets = []
            for r, c in self.targets:
                if row == r and col == c:
                    targets = [(row, col)]
                    row, col = self.origin
                    self.targets = []
                    break
        else:  
            targets = get_targets(row, col)
    
        if targets == []:
            # no targets, nothing to do
            print('No valid moves.')

        elif len(targets) > 1:
            print('Possible targets', [rc2a1(r, c) for r, c in targets])
            self.targets = targets
            self.origin = (row, col)
        else:
            # only 1 target, make the move
            row_target, col_target = targets[0]
            row_kill, col_kill = int((row + row_target) / 2), int((col + col_target) / 2)
            board[row][col] = 0
            board[row_target][col_target] = 1
            board[row_kill][col_kill] = 0
            print('Move', rc2a1(row, col), 'to', rc2a1(row_target, col_target))
            draw()
        
        self.update()
        
    def keyPressEvent(self, e):
        # press R to reset
        if e.key() == QtCore.Qt.Key_R:
            global board
            board = copy.deepcopy(board0)
            self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtCore.Qt.blue)

        # background
        qp.fillRect(0, 0, 490, 490, QtCore.Qt.white)
        
        # draw the grid
        qp.drawLine(140,   0, 350,   0)
        qp.drawLine(140,  70, 350,  70)
        qp.drawLine(  0, 140, 490, 140)
        qp.drawLine(  0, 210, 490, 210)
        qp.drawLine(  0, 280, 490, 280)
        qp.drawLine(  0, 350, 490, 350)
        qp.drawLine(140, 420, 350, 420)
        qp.drawLine(140, 490, 350, 490)

        qp.drawLine(  0, 140,   0, 350)
        qp.drawLine( 70, 140,  70, 350)
        qp.drawLine(140,   0, 140, 490)
        qp.drawLine(210,   0, 210, 490)
        qp.drawLine(280,   0, 280, 490)
        qp.drawLine(350,   0, 350, 490)
        qp.drawLine(420, 140, 420, 350)
        qp.drawLine(490, 140, 490, 350)

        # draw the pegs
        s = 50
        y = 10
        for row in board:
            x = 10
            for peg in row:
                if peg == 1:
                    qp.drawEllipse(x, y, s, s)
                x += 70
            y += 70

        # special mode - draw targets if multiple are possible
        if not self.targets == []:
            qp.setPen(QtCore.Qt.red)
            for row, col in self.targets:
                x, y = 70 * col, 70 * row
                qp.drawLine(x, y, x + 70, y)
                qp.drawLine(x, y, x, y + 70)
                qp.drawLine(x + 70, y, x + 70, y + 70)
                qp.drawLine(x, y + 70, x + 70, y + 70)
            
        #qp.drawText(10, 20, f'Disks: {self.N}')
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
