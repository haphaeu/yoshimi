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

        self.materials = [['Steel', 7850, 210],
                     ['Aluminium', 1, 2],
                     ['Titanium', 3, 4],
                     ['Custom', 0, 0]]  # leave Custom at the end

         # tests
         #self.comboMaterial = QtGui.QComboBox(self)
         #self.test = QtGui.QLineEdit(self)
         #self.test.

         # set up combo box
        for mat in self.materials:
            self.comboMaterial.addItem(mat[0])
        self.comboMaterial.activated.connect(self.comboMaterialChange)
        
        self.lineOD.textChanged.connect(self.calc_wt)
        self.lineID.textChanged.connect(self.calc_wt)
        
        self.lineOD.setText('125.4')
        self.lineID.setText('100.0') 
        
        self.comboMaterialChange(0)
        
        self.buttonAddRow.clicked.connect(self.addRow)
        self.buttonDelRow.clicked.connect(self.delRow)
        self.buttonAddCol.clicked.connect(self.addCol)
        self.buttonDelCol.clicked.connect(self.delCol)
        
        headers = ('OD [mm]', 'ID [mm]', 'WT [mm]',
                   'Material Density [kg/m³]', 'Material Modulus [GPa]',
                   'Coating Thickness [mm]', 'Coating Density [kg/m³]',
                   'Liner Thickness [mm]', 'Liner Density [kg/m³]',
                   'Axial Stiffness [kN]',
                   'Bending Stiffness [kN.m²]',
                   'Torsional Stiffness [kN.m²]',
                   'Weight in air, empty [kg/m]',
                   'Weight in air, filled [kg/m]',
                   'Weight in water, filled [kg/m]')
        for i, h in enumerate(headers):
            self.table.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(h))
        
        headers = ('8in pipe', '12in pipe')
        for i, h in enumerate(headers):
            self.table.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(h))
    
        self.table.cellChanged.connect(self.do_calcs)
        
        self.table = QtGui.QTableWidget()
        #self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    
    def comboMaterialChange(self, idx):
        if idx == len(self.materials)-1:
            # custom
            self.lineMaterialDensity.setEnabled(True)
            self.lineMaterialModulus.setEnabled(True)
            #self.lineMaterialDensity.setText('')
            #self.lineMaterialModulus.setText('')
        else:
            # material from database
            self.lineMaterialDensity.setEnabled(False)
            self.lineMaterialModulus.setEnabled(False)           
            self.lineMaterialDensity.setText(str(self.materials[idx][1]))
            self.lineMaterialModulus.setText(str(self.materials[idx][2]))
            self.calc_wt()
    
    def do_calcs(self, row, col):
        self.table.setItem(row+1, col, QtGui.QTableWidgetItem('test'))        
        
    def calc_wt(self):
        try:
            self.lineWT.setText('%.4f' % ((float(self.lineOD.text()) - 
                               float(self.lineID.text()))/2))
        except:
            self.lineWT.setText('nan')
       
    def addRow(self):
        self.table.setRowCount(self.table.rowCount()+1)

    def delRow(self):
        self.table.setRowCount(self.table.rowCount()-1)
        
    def addCol(self):
        self.table.setColumnCount(self.table.columnCount()+1)

    def delCol(self):
        self.table.setColumnCount(self.table.columnCount()-1)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())