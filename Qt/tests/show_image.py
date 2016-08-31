# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:25:01 2016

@author: rarossi
"""

import sys
from PyQt4 import QtGui
app = QtGui.QApplication(sys.argv)
window = QtGui.QMainWindow()
window.setGeometry(0, 0, 400, 200)
pic = QtGui.QLabel(window)
pic.setGeometry(10, 10, 400, 200)
pixmap = QtGui.QPixmap('maze.bmp')
pixmap = pixmap.scaledToHeight(200)
pic.setPixmap(pixmap)

window.show()
sys.exit(app.exec_())
