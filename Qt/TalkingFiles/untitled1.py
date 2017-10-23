# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 13:04:56 2017

@author: rarossi
"""
import subprocess
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

import math


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        self.btn = QtGui.QPushButton('Run')
        grid.addWidget(self.btn, 1, 1)

        self.txt = QtGui.QTextEdit()
        grid.addWidget(self.txt, 1, 2)

        self.btn.clicked.connect(self.run_stream)

        self.setWindowTitle('Capture Stream')
        self.resize(400, 200)
        self.show()

    def run_stream(self):
        self.btn.blockSignals(True)
        self.btn.setEnabled(False)
        cmd = r'C:\Users\rarossi\Anaconda3\python.exe stream.py 6'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        for line in iter(p.stdout.readline, b''):
            self.txt.append(line.decode().replace('\r\n', ''))
            self.repaint()
        self.btn.setEnabled(True)
        self.btn.blockSignals(False)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
