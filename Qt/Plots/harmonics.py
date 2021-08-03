  # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

import math

_TAU = 2*math.pi

class Example(QtWidgets.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
 
        self.xspin1 = QtWidgets.QSlider()
        self.xspin1.setMaximum(1000)
        self.xspin1.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.xspin1, 1, 2)
        
        self.xspin2 = QtWidgets.QSlider()
        self.xspin2.setMaximum(1000)        
        self.xspin2.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.xspin2, 2, 2)
        
        self.yspin1 = QtWidgets.QSlider()
        self.yspin1.setOrientation(QtCore.Qt.Vertical)
        grid.addWidget(self.yspin1, 0, 0)
        
        self.yspin2 = QtWidgets.QSlider()
        self.yspin2.setOrientation(QtCore.Qt.Vertical)
        grid.addWidget(self.yspin2, 0, 1)
        

        
        self.xspin1.setValue(440)
        self.yspin1.setValue(25)
        self.xspin2.setValue(650)
        self.yspin2.setValue(41)

        
        self.yspin1.valueChanged.connect(self.changes)
        self.yspin2.valueChanged.connect(self.changes)
        self.xspin1.valueChanged.connect(self.changes)
        self.xspin2.valueChanged.connect(self.changes)

        self.setWindowTitle('Two harmonics')
        self.resize(400, 200)
        self.show()
    
    def changes(self):
        print(self.xspin1.value(), self.yspin1.value(),
              self.xspin2.value(), self.yspin2.value())
        self.update()
    
    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawGrid(qp)
        self.draw(qp)
        qp.end()
        
    def drawGrid(self, qp):
        
        qp.setPen(QtCore.Qt.gray)
        size = self.size()
        w, h = size.width(), size.height()
        
        for x in range(0, w, 100):
            qp.drawLine(x, 0, x, h)
        
        ho2 = h//2
        for y in range(0, ho2, 100):
            qp.drawLine(0, ho2-y, w, ho2-y)
            qp.drawLine(0, ho2+y, w, ho2+y)
        
    def draw(self, qp):
      
        qp.setPen(QtCore.Qt.black)
        size = self.size()
        w, h = size.width(), size.height()
        
        A1 = self.yspin1.value()/100*h/2
        o1 = self.xspin1.value()/10000
        A2 = self.yspin2.value()/100*h/2
        o2 = self.xspin2.value()/10000
        t1 = _TAU/o1 if o1 > 0 else 0
        t2 = _TAU/o2 if o2 > 0 else 0
        qp.drawText(QtCore.QRect(0, 0, w-10, h), QtCore.Qt.AlignRight, 
                    '{0:.1f}, {1:.1f} / {2:.1f}, {3:.1f}'.format(A1, t1, 
                                                                 A2, t2))
        
        xo, yo = 0, h/2
        for i in range(w):
            #self.prog.setValue(99)
            x = i
            y = A1 * math.sin(o1*x) + A2 * math.sin(o2*x)+ h/2
            qp.drawLine(xo, yo, x, y) 
            xo, yo = x, y

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()