# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 13:04:56 2017

@author: rarossi
"""
import subprocess
import sys
from PyQt5 import QtGui, QtCore, QtWidgets


class Example(QtWidgets.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        self.btn = QtWidgets.QPushButton('Run')
        grid.addWidget(self.btn, 1, 1)

        self.txt = QtWidgets.QTextEdit()
        grid.addWidget(self.txt, 1, 2)

        self.btn.clicked.connect(self.run_stream)
        
        self.setWindowTitle('Capture Stream')
        self.resize(400, 200)
        self.show()

    def run_stream(self):
        #
        # this should be moved to a thread...
        #
        cmd = 'python stream.py 6'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        for line in iter(p.stdout.readline, b''):
            self.txt.append(line.decode().replace('\n', '').replace('\r', ''))
            self.repaint()
            
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
