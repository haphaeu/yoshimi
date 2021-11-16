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
board_hist = [copy.deepcopy(board)]

solve_sequence = [
    # sequence of moves in the form (row_from, col_from, row_to, col_to)
    (5, 3, 3, 3), (4, 5, 4, 3), (6, 4, 4, 4), (6, 2, 6, 4), (3, 4, 5, 4),
    (6, 4, 4, 4), (1, 4, 3, 4), (2, 6, 2, 4), (4, 6, 2, 6), (2, 3, 2, 5),
    (2, 6, 2, 4), (2, 1, 2, 3), (0, 2, 2, 2), (0, 4, 0, 2), (3, 2, 1, 2),
    (0, 2, 2, 2), (5, 2, 3, 2), (4, 0, 4, 2), (2, 0, 4, 0), (4, 3, 4, 1),
    (4, 0, 4, 2), (2, 3, 2, 1), (2, 1, 4, 1), (4, 1, 4, 3), (4, 3, 4, 5),
    (4, 5, 2, 5), (2, 5, 2, 3), (3, 3, 3, 1), (1, 3, 3, 3), (3, 4, 3, 2),
    (3, 1, 3, 3),
]


def rc2a1(row, col):
    return '%s%d' % ('ABCDEFG'[col], row + 1)

def reset():
    global board
    global board_hist
    board = copy.deepcopy(board0)
    board_hist = [copy.deepcopy(board)]

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
    possible_targets = []
    for candidate_row, candidate_col in potential_targets:
        if is_valid_move(row, col, candidate_row, candidate_col):
            possible_targets.append((candidate_row, candidate_col))
    return possible_targets

def is_valid_move(row, col, row_target, col_target):
    row_kill, col_kill = (row + row_target)//2, (col + col_target)//2
    return (
        0 <= row < 7
        and 0 <= col < 7
        and board[row][col] == 1
        and 0 <= row_target < 7
        and 0 <= col_target < 7
        and board[row_target][col_target] == 0
        and board[row_kill][col_kill] == 1
    )

def get_all_possible_moves():
    moves = {}
    for i, row in enumerate(board):
        for j, peg in enumerate(row):
            targets = get_targets(i, j)
            if targets:
                moves[(i, j)] = targets
    return moves

def make_move(row, col, row_target, col_target):
    if is_valid_move(row, col, row_target, col_target):
        row_kill, col_kill = (row + row_target)//2, (col + col_target)//2
        board[row][col] = 0
        board[row_target][col_target] = 1
        board[row_kill][col_kill] = 0
        board_hist.append(copy.deepcopy(board))
        return True
    return False

def solve(flag_draw=False):
    for move in solve_sequence:
        make_move(*move)
        if flag_draw:
            draw()
    return score()

def noob(flag_draw=False):
    import random
    reset()
    moves = []
    while get_all_possible_moves():
        move = [random.randrange(0, 7) for i in range(4)]
        if make_move(*move):
            moves.append(move)
        if flag_draw:
            draw()
    return moves, score()

def solve_noob():
    i, score = 0, 0
    while score < 51:
        moves, score = noob()
        i += 1
    print(i)
    print(moves)
    draw()

    
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

def score():
    total = 0
    for row in board:
        total += row.count(1)
    return 100 / total

class Window(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        self.mousePressEvent = self.mouse_clicked
        
        self.setWindowTitle('Resta Um')
        self.setMinimumSize(490, 490)

        # Help vars used for selection of multiple targets
        self.targets = []
        self.origin = 0, 0

        print('### ######## ###')
        print('### Resta Um ###')
        print('### ######## ###')
        print('R to reset.')
        print('B to go back one move.')
        print('######################')

        self.show_ascii_board = False

        if self.show_ascii_board:
            draw()
        
        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.w = self.size().width()  # window width
        self.h = self.size().height() # window height
        self.l = min(self.w, self.h)  # board size
        self.c = self.l // 7  # cell size
        self.ox = (self.w - self.l) // 2  # x offset
        self.oy = (self.h - self.l) // 2 # y offset
        
    def mouse_clicked(self, event):
        x = event.pos().x()
        y = event.pos().y()
        row = (y - self.oy) // self.c
        col = (x - self.ox) // self.c
        self.move(row, col)

    def move(self, row, col):

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
            print('No valid moves for', row, col)

        elif len(targets) > 1:
            print('Possible targets for', row, col, ':', targets)
            self.targets = targets
            self.origin = (row, col)
        else:
            # only 1 target, make the move
            row_target, col_target = targets[0]
            make_move(row, col, row_target, col_target)
            print('Move', row, col, 'to', row_target, col_target)
            if self.show_ascii_board:
                draw()
        
        self.update()
        
    def keyPressEvent(self, e):
        global board
        global board_hist
        if e.key() == QtCore.Qt.Key_R:
            print('Reset board.')
            board = copy.deepcopy(board0)
            board_hist = [copy.deepcopy(board)]
            draw()
            self.update()
        elif e.key() == QtCore.Qt.Key_B:
            if len(board_hist) == 1:
                print('Nothing to undo.')
            else:
                print('Undo last move.')
                board_hist.pop()
                board = copy.deepcopy(board_hist[-1])
                draw()
                self.update()
        elif e.key() == QtCore.Qt.Key_A:
            self.solve_me()
            
    def solve_me(self):
        global board
        global board_hist
        board = copy.deepcopy(board0)
        board_hist = [copy.deepcopy(board)]
        self.update()
        for move in solve_sequence:
            QtTest.QTest.qWait(500)
            make_move(*move)
            draw()
            self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        pen = qp.pen()
        
        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtCore.Qt.darkRed)

        w = self.w
        h = self.h
        c = self.c
        ox, oy = self.ox, self.oy
        
        # background
        qp.fillRect(0, 0, w, h, QtCore.Qt.white)
        
        # draw the board borders
        pen.setWidth(5)
        qp.setPen(pen)
        qp.drawLine(2*c + ox, 0*c + oy, 5*c + ox, 0*c + oy)
        qp.drawLine(2*c + ox, 7*c + oy, 5*c + ox, 7*c + oy)
        qp.drawLine(0*c + ox, 2*c + oy, 0*c + ox, 5*c + oy)
        qp.drawLine(7*c + ox, 2*c + oy, 7*c + ox, 5*c + oy)
        qp.drawLine(0*c + ox, 2*c + oy, 2*c + ox, 2*c + oy)
        qp.drawLine(5*c + ox, 2*c + oy, 7*c + ox, 2*c + oy)
        qp.drawLine(0*c + ox, 5*c + oy, 2*c + ox, 5*c + oy)
        qp.drawLine(5*c + ox, 5*c + oy, 7*c + ox, 5*c + oy)
        qp.drawLine(2*c + ox, 0*c + oy, 2*c + ox, 2*c + oy)
        qp.drawLine(2*c + ox, 5*c + oy, 2*c + ox, 7*c + oy)
        qp.drawLine(5*c + ox, 0*c + oy, 5*c + ox, 2*c + oy)
        qp.drawLine(5*c + ox, 5*c + oy, 5*c + ox, 7*c + oy)

        # Inner grid
        pen.setWidth(1)
        qp.setPen(pen)
        qp.drawLine(2*c + ox, 1*c + oy, 5*c + ox, 1*c + oy)
        qp.drawLine(2*c + ox, 2*c + oy, 5*c + ox, 2*c + oy)
        qp.drawLine(0*c + ox, 3*c + oy, 7*c + ox, 3*c + oy)
        qp.drawLine(0*c + ox, 4*c + oy, 7*c + ox, 4*c + oy)
        qp.drawLine(2*c + ox, 5*c + oy, 5*c + ox, 5*c + oy)
        qp.drawLine(2*c + ox, 6*c + oy, 5*c + ox, 6*c + oy)
        qp.drawLine(1*c + ox, 2*c + oy, 1*c + ox, 5*c + oy)
        qp.drawLine(2*c + ox, 2*c + oy, 2*c + ox, 5*c + oy)
        qp.drawLine(3*c + ox, 0*c + oy, 3*c + ox, 7*c + oy)
        qp.drawLine(4*c + ox, 0*c + oy, 4*c + ox, 7*c + oy)
        qp.drawLine(5*c + ox, 2*c + oy, 5*c + ox, 5*c + oy)
        qp.drawLine(6*c + ox, 2*c + oy, 6*c + ox, 5*c + oy)
        
        # draw the pegs
        s = 2 * c // 4
        y = oy + (c - s) // 2
        for row in board:
            x = ox + (c - s) // 2
            for peg in row:
                if peg == 1:
                    qp.drawEllipse(x, y, s, s)
                x += c
            y += c

        # special mode - draw targets if multiple are possible
        if not self.targets == []:
            qp.setPen(QtCore.Qt.red)
            pen = qp.pen()
            pen.setWidth(2)
            qp.setPen(pen)
            qp.setBrush(QtCore.Qt.lightGray)
            for row, col in self.targets:
                x, y = ox + c * col, oy + c * row
                qp.drawEllipse(x + (c - s) // 2, y + (c - s) // 2, s, s)
                qp.drawLine(x, y, x + c, y)
                qp.drawLine(x, y, x, y + c)
                qp.drawLine(x + c, y, x + c, y + c)
                qp.drawLine(x, y + c, x + c, y + c)
            
        qp.drawText(10, 20, 'Score: %.1f%%' % score())
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
