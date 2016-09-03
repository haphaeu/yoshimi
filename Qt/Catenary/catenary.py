# -*- coding: utf-8 -*-
"""

Catenary
========

This is an upgrade to Python/PyQt4 of the old app written back in October 2010 using
VB/MS Visual Studio.

Created on 3 Sep 2016, FUCKING TWICE after file got corrupted after 100% done...

@author: raf
"""

import sys
from math import cosh
from PyQt4 import QtCore, QtGui, uic
import catenarylib as cat

qtCreatorFile = 'catenary.ui'  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.default_w = 150

        self.lineTA.setText('12.000')
        self.lineV.setText('1800.000')

        self.lineTA.textChanged.connect(self.changed)
        self.lineV.textChanged.connect(self.changed)
        self.lineH.textChanged.connect(self.changed)
        self.lineL.textChanged.connect(self.changed)
        self.lineMBR.textChanged.connect(self.changed)

        self.btnCalc.clicked.connect(self.calc)
        self.btnClear.clicked.connect(self.clear)
        self.btnPlot.clicked.connect(self.plot)

        self.plotReady = False
        self.btnPlot.setEnabled(False)

    def clear(self):
        self.lineTA.setText('')
        self.lineV.setText('')
        self.lineH.setText('')
        self.lineL.setText('')
        self.lineMBR.setText('')

    def changed(self):
        self.btnPlot.setEnabled(False)
        self.plotReady = False
        self.update()

    def getParams(self):
        try:
            self.TA = float(self.lineTA.text())
        except:
            self.TA = 0
        try:
            self.V = float(self.lineV.text())
        except:
            self.V = 0
        try:
            self.H = float(self.lineH.text())
        except:
            self.H = 0
        try:
            self.L = float(self.lineL.text())
        except:
            self.L = 0
        try:
            self.MBR = float(self.lineMBR.text())
        except:
            self.MBR = 0

    def setParams(self):
        self.lineTA.setText('%.3f' % self.TA)
        self.lineV.setText('%.3f' % self.V)
        self.lineH.setText('%.3f' % self.H)
        self.lineL.setText('%.3f' % self.L)
        self.lineMBR.setText('%.3f' % self.MBR)
        self.btnPlot.setEnabled(True)

    def errInput(self, msg):
        QtGui.QMessageBox.critical(self, "Input error", msg)
        self.flagErr = True

    def calc(self):
        """read input boxes and calls catenary calculations"""
        self.getParams()
        TA, V, H, L, MBR = self.TA, self.V, self.H, self.L, self.MBR
        self.flagErr = False

        if TA > 0:
            if V > 0: TA, V, H, L, MBR = cat.CatenaryCalcTAV(TA, V)
            elif H > 0: TA, V, H, L, MBR = cat.CatenaryCalcTAH(TA, H)
            elif L > 0: TA, V, H, L, MBR = cat.CatenaryCalcTAL(TA, L)
            elif MBR > 0: TA, V, H, L, MBR = cat.CatenaryCalcTAMBR(TA, MBR)
            else: self.errInput('Two parameters should be input.')
        else:  # case TA not input
            if V > 0:
                if H > 0: TA, V, H, L, MBR = cat.CatenarySolveV_HLMBR(V, H, 'h')

                elif L > 0:
                    if L <= V: self.errInput('Error in input values. L <= V.')
                    else: TA, V, H, L, MBR = cat.CatenarySolveV_HLMBR(V, L, 'l')
                elif MBR > 0: TA, V, H, L, MBR = cat.CatenarySolveV_HLMBR(V, MBR, 'mbr')
                else: self.errInput('Two parameters should be input.')
            elif H > 0:
                if L > 0:
                    if L <= H: self.errInput('Error in input values. L <= H.')
                    else: TA, V, H, L, MBR = cat.CatenarySolveH_LMBR(H, L, 'l')
                elif MBR > 0: TA, V, H, L, MBR = cat.CatenarySolveH_LMBR(H, MBR, 'mbr')
                else: self.errInput('Two parameters should be input.')
            elif L > 0:
                if MBR > 0: TA, V, H, L, MBR = cat.CatenarySolveL_MBR(L, MBR)
                else: self.errInput('Two parameters should be input.')
            else:  # all input parameters are =0
                self.errInput('Two parameters should be input.')

        if not self.flagErr:
            self.TA, self.V, self.H, self.L, self.MBR = TA, V, H, L, MBR
            self.setParams()

    def plot(self):
        if self.size().width() <= self.default_w+200:
            self.resize(self.default_w+200, self.size().height())
        self.CalculatePoints()
        self.plotReady = True
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
        if self.plotReady:
            self.CalcDrawCatenary()
            self.draw(qp)
        else:
            qp.eraseRect(0, 0, 9999, 9999)
        qp.end()

    def draw(self, qp):
        for i in range(self.NoPts-1):
            qp.drawLine(self.cvX[i], self.cvY[i], self.cvX[i+1], self.cvY[i+1])

    def CalculatePoints(self):
        """Calculate the catenary points in the input coordinates"""

        self.NoPts = 100

        self.Xmin = 0.0
        self.Xmax = self.H
        xstep = (self.Xmax - self.Xmin) / (self.NoPts - 1)
        X, Y = [0]*self.NoPts, [0]*self.NoPts
        self.normX, self.normY = [0]*self.NoPts, [0]*self.NoPts
        self.Ymin = self.MBR
        self.Ymax = self.MBR + self.V
        rangeX = self.Xmax - self.Xmin
        rangeY = self.Ymax - self.Ymin

        for i in range(self.NoPts):
            # points in catenary scale
            X[i] = self.Xmin + i * xstep
            Y[i] = self.MBR * cosh(X[i] / self.MBR)
            # normalised points, from 0 to 1
            # these will be resized to draw in canvas
            self.normX[i] = (X[i] - self.Xmin) / rangeX
            self.normY[i] = -(Y[i] - self.Ymax) / rangeY

    def CalcDrawCatenary(self):
        """Calculate the points to be drawn in the canvas
        The aspect ratio of the real catenary is preserved
        """
        w, h = self.size().width() - self.default_w, self.size().height()

        # Calculate aspect ratio of the Catenary and the Canvas
        CatenaryAspectRatio = (self.Xmax - self.Xmin) / (self.Ymax - self.Ymin)
        BorderW = 10
        BorderH = 10
        CanvasW = w - 2 * BorderW
        CanvasH = h - 2 * BorderH
        CanvasAspectRatio = CanvasW / CanvasH
        # Calculate the multiplication and shift to be applied to the points
        # so that the fit the canvas keeping the original catenary aspect ratio
        if CatenaryAspectRatio > CanvasAspectRatio:
            Xfactor = 1.0
            Xshift = BorderW
            Yfactor = CanvasAspectRatio / CatenaryAspectRatio
            Yshift = (1 - Yfactor) * CanvasH / 2 + BorderH
        elif CatenaryAspectRatio < CanvasAspectRatio:
            Xfactor = CatenaryAspectRatio / CanvasAspectRatio
            Xshift = (1 - Xfactor) * CanvasW / 2 + BorderW
            Yfactor = 1.0
            Yshift = BorderH
        else:
            Xfactor = 1.0
            Xshift = BorderW
            Yfactor = 1.0
            Yshift = BorderH

        # draw on the right side of the input boxes
        Xshift += self.default_w

        # and finally, calculates the points to be drawn in the canvas
        # by multipling the normalized points to the factors and shifts
        self.cvX, self.cvY = [0]*self.NoPts, [0]*self.NoPts
        # allocate memory for the points to plot
        for i in range(self.NoPts):
            self.cvX[i] = self.normX[i] * CanvasW * Xfactor + Xshift
            self.cvY[i] = self.normY[i] * CanvasH * Yfactor + Yshift


def main():
    app = QtGui.QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
