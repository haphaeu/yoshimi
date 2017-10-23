# -*- coding: utf-8 -*-
"""

Resposta a minha pergunta:

https://stackoverflow.com/a/46817275/5069105

Created on Thu Oct 19 08:36:41 2017

@author: rarossi
"""

import sys
from PyQt4 import QtGui, QtCore


class Thread(QtCore.QThread):
    def run(self):
        QtCore.QThread.sleep(2)


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
        self.btn = QtGui.QPushButton('Count')
        grid.addWidget(self.btn, 1, 1)
        self.txt1 = QtGui.QTextEdit()
        grid.addWidget(self.txt1, 1, 2)
        self.btn.clicked.connect(self.click)
        self.thread = Thread()
        self.thread.finished.connect(lambda: self.btn.setEnabled(True))
        self.show()

    def click(self):
        self.txt1.append('click')
        if not self.thread.isRunning():
            self.btn.setEnabled(False)
            self.thread.start()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
