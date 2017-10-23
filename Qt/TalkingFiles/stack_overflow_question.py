# -*- coding: utf-8 -*-
"""
Este é um exemplo mínimo para uma pergunta no stackoverflow:

https://stackoverflow.com/questions/46811610/pyqt-how-to-disable-multiple-clicks-for-qpushbutton

Created on Wed Oct 18 15:25:54 2017

@author: rarossi
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 13:04:56 2017

@author: rarossi
"""
import time
import sys
from PyQt4 import QtGui

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
        self.count = 0
        self.show()

    def click(self):
        # Here I want to block any further click in the button, but it is
        # not working - clicking it 10 times quickly will run this 10 times...
        self.btn.blockSignals(True)
        self.btn.setEnabled(False)
        time.sleep(2)  # time consuming code...
        self.count += 1
        self.txt1.append(str(self.count))
        self.repaint()
        self.btn.setEnabled(True)
        self.btn.blockSignals(False)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
