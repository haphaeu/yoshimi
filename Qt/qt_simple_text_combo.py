# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 18:29:14 2016

@author: raf
"""

import sys
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = 'untitled.ui'  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.boxOD.textChanged.connect(self.calc_wt)
        self.boxID.textChanged.connect(self.calc_wt)
        
        self.boxOD.setText('125.4')
        self.boxID.setText('100.0') 
    
    def calc_wt(self):
        try:
            self.boxWT.setText('%.4f' % ((float(self.boxOD.text()) - 
                               float(self.boxID.text()))/2))
        except:
            self.boxWT.setText('nan')
            

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())