# -*- coding: utf-8 -*-
"""

Elastic collisions between 2 blocks and 1 wall.

See collisions.py

@author: rarossi
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter
import time
import numpy as np
import logging

from collisions import Block, System

LOGGING_LEVEL_MAIN = logging.INFO
LOGGING_LEVEL_DATA = logging.INFO
LOGGING_LEVEL_GAME = logging.INFO
logging.basicConfig()


class DataThread(QtCore.QThread):

    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(LOGGING_LEVEL_DATA)
        self.b1 = Block(m=1, v=0, x=400, a=10)
        self.b2 = Block(m=9, v=-0.5, x=550, a=20)
        sys = System(self.b1, self.b2)
        self.max_iters = sys.max_iters
        self.sys = sys
        self.data = np.ones(shape=(self.max_iters+1, 5)) * 999_999
        self.data[0, :] = sys.t, sys.b1.x, sys.b1.v, sys.b2.x, sys.b2.v
        self.status = 'init'
        self.logger.info(f'{self.__class__.__name__} initialised.')

    def run(self):
        sys = self.sys
        self.status = 'running'
        self.logger.info(f'{self.__class__.__name__} running.')
        while True:
            sys.iterate()
            sys.num_iters += 1
            self.data[sys.num_iters, :] = sys.t, sys.b1.x, sys.b1.v, sys.b2.x, sys.b2.v
            self.logger.debug(self.data[sys.num_iters, :])
            if sys.stop_simulation():
                self.logger.info('stop sim criteria reached')
                break
            if sys.num_iters >= self.max_iters:
                self.logger.info('reached max iters')
                break
        self.status = 'stopped'
        self.logger.info(f'{self.__class__.__name__} stopped.')


class WorkThread(QtCore.QThread):

    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(LOGGING_LEVEL_GAME)
        self.t = 0
        self.dt = 0.1
        self.data_now = 0, 0, 0, 0, 0
        self.status = 'init'
        self.logger.info(f'{self.__class__.__name__} initialised.')

    def run(self):
        data = self.parent.data.data
        self.status = 'running'
        self.logger.info(f'{self.__class__.__name__} running.')
        while True:
            idx = np.where(data[:, 0] <= self.t)[0][-1]
            self.data_now = data[idx, :]
            self.logger.debug((self.t, idx, self.data_now, data[:,0]))
            self.parent.update()
            #time.sleep(self.dt)
            self.t += self.dt
            if self.t >= self.parent.data.sys.t:
                break
        self.status = 'stopped'
        self.logger.info(f'{self.__class__.__name__} stopped.')


class Window(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(LOGGING_LEVEL_MAIN)
        self.init()
        self.initUI()

    def init(self):
        self.data = DataThread(self)
        self.game = WorkThread(self)
        self.data.start()
        self.game.start()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.setWindowTitle('Collisions')
        self.setMinimumSize(800, 100)
        self.logger.info('UI initialised.')
        self.show()
        
    def keyPressEvent(self, e):
        # press R to reset
        if e.key() == QtCore.Qt.Key_R:
            if self.game.status == 'stopped' and self.data.status == 'stopped':
                self.logger.info('Key R pressed - resetting game.')
                del self.game
                del self.data
                self.init()
            else:
                self.logger.info('Key R pressed - threads still running - wait.')

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        qp.setPen(QtCore.Qt.black)

        h = self.size().height()
        w = self.size().width()
        
        ground_y = 50
        
        # draw the ground and wall
        qp.drawLine(0, ground_y, w, ground_y)
        qp.fillRect(0, 0, 3, ground_y, QtCore.Qt.black)
        
        # draw the blocks
        a1, a2 = int(self.data.b1.a), int(self.data.b2.a)
        t, x1, v1, x2, v2 = self.game.data_now
        x1, x2 = int(x1), int(x2)
        qp.fillRect(x1-a1, ground_y-2*a1, 2*a1, 2*a1, QtCore.Qt.yellow)
        qp.drawRect(x1-a1, ground_y-2*a1, 2*a1, 2*a1)
        qp.fillRect(x2-a2, ground_y-2*a2, 2*a2, 2*a2, QtCore.Qt.green)
        qp.drawRect(x2-a2, ground_y-2*a2, 2*a2, 2*a2)
        
        qp.setPen(QtCore.Qt.gray)
        qp.drawText(    5, h- 5, f'Block 2 v: {v2:+.3f}, x: {x2:.0f}')
        qp.drawText(    5, h-20, f'Block 1 v: {v1:+.3f}, x: {x1:.0f}')
        qp.drawText( w//2, h- 5, f'System iteractions: {self.data.sys.num_iters}')
        qp.drawText( w//2, h-20, f'Block collisions: {self.data.sys.num_collisions}')
        qp.drawText(w-120, h- 5, 'Data thread: %s' % self.data.status)
        qp.drawText(w-120, h-20, 'Game thread: %s' % self.game.status)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

