# -*- coding: utf-8 -*-
"""

Pipe Properties
===============

Calculate cross sectional properties and weights in air and in water for homogeneous pipes.

This is an upgrade to Python/PyQt4 of the old app written back in October 2010 using
VB/MS Visual Studio.

Created on Wed Aug 10 18:29:14 2016

Updated 23.09.2017 - included options for 2 external coatings

@author: raf
"""

import sys
from PyQt4 import QtCore, QtGui, uic
from numpy import pi

qtCreatorFile = 'pipe_properties.ui'  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.materials = [  # density, modulus, poisson
                         ['Steel',     7850, 200, 0.29],
                         ['Aluminium', 2800,  69, 0.33],
                         ['Titanium',  4400, 120, 0.32],
                         ['Concrete',  2300,  20, 0.20],
                         ['Custom', 0, 0, 0]]  # leave Custom at the end

        # tests
        # self.comboMaterial = QtGui.QComboBox(self)
        # self.test = QtGui.QLineEdit(self)
        # self.test.

        # set up combo box
        for mat in self.materials:
            self.comboMaterial.addItem(mat[0])
        self.comboMaterial.activated.connect(self.comboMaterialChange)

        self.lineOD.setText('125.4')
        self.lineID.setText('100.0')
        self.lineWT.setText('0.0')
        self.lineCoatingThickness.setText('0.0')
        self.lineCoatingDensity.setText('0.0')
        self.lineCoating2Thickness.setText('0.0')
        self.lineCoating2Density.setText('0.0')
        self.lineLinerThickness.setText('0.0')
        self.lineLinerDensity.setText('0.0')
        self.lineContentsDensity.setText('0.0')

        # note that this read only style is also hard coded inside self.cell()
        self.readOnlyBackgroundStyle = 'background-color: rgb(216, 216, 216);'
        self.defaultBackgroundStyle = 'background-color: rgb(255, 255, 255);'

        self.lineWT.setReadOnly(True)
        self.lineWT.setStyleSheet(self.readOnlyBackgroundStyle)

        self.lineAxialStiffness.setReadOnly(True)
        self.lineBendingStiffness.setReadOnly(True)
        self.lineTorsionalStiffness.setReadOnly(True)
        self.lineWeightDryEmpty.setReadOnly(True)
        self.lineWeightDryFilled.setReadOnly(True)
        self.lineWeightWetFilled.setReadOnly(True)

        self.lineAxialStiffness.setStyleSheet(self.readOnlyBackgroundStyle)
        self.lineBendingStiffness.setStyleSheet(self.readOnlyBackgroundStyle)
        self.lineTorsionalStiffness.setStyleSheet(self.readOnlyBackgroundStyle)
        self.lineWeightDryEmpty.setStyleSheet(self.readOnlyBackgroundStyle)
        self.lineWeightDryFilled.setStyleSheet(self.readOnlyBackgroundStyle)
        self.lineWeightWetFilled.setStyleSheet(self.readOnlyBackgroundStyle)

        self.comboMaterialChange(0)

        self.lineOD.textChanged.connect(self.calc_simple)
        self.lineID.textChanged.connect(self.calc_simple)
        self.lineWT.textChanged.connect(self.calc_simple)
        self.lineCoatingThickness.textChanged.connect(self.calc_simple)
        self.lineCoatingDensity.textChanged.connect(self.calc_simple)
        self.lineCoating2Thickness.textChanged.connect(self.calc_simple)
        self.lineCoating2Density.textChanged.connect(self.calc_simple)
        self.lineLinerThickness.textChanged.connect(self.calc_simple)
        self.lineLinerDensity.textChanged.connect(self.calc_simple)
        self.lineMaterialModulus.textChanged.connect(self.calc_simple)
        self.lineMaterialDensity.textChanged.connect(self.calc_simple)
        self.lineMaterialPoisson.textChanged.connect(self.calc_simple)
        self.lineContentsDensity.textChanged.connect(self.calc_simple)

        self.radioOD.clicked.connect(self.toggle_OD_ID_WT)
        self.radioID.clicked.connect(self.toggle_OD_ID_WT)
        self.radioWT.clicked.connect(self.toggle_OD_ID_WT)

        self.buttonAddCol.clicked.connect(self.addCol)
        self.buttonDelCol.clicked.connect(self.delCol)
        self.buttonCopyCol.clicked.connect(self.copyCol)

        # set up the table
        self.table.horizontalHeader().setVisible(True)
        self.table.verticalHeader().setVisible(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        headers = ('OD [mm]', 'ID [mm]', 'WT [mm]',
                   'Material Density [kg/m³]', 'Material Modulus [GPa]', 'Poisson Ratio',
                   'Contents Density [kg/m³]', 'Coating Thickness [mm]', 'Coating Density [kg/m³]', 
                   'Coating 2 Thickness [mm]', 'Coating 2 Density [kg/m³]',
                   'Liner Thickness [mm]', 'Liner Density [kg/m³]',
                   'Axial Stiffness [kN]',
                   'Bending Stiffness [kN.m²]',
                   'Torsional Stiffness [kN.m²]',
                   'Weight in air, empty [kg/m]',
                   'Weight in air, filled [kg/m]',
                   'Weight in water, filled [kg/m]')

        self.table.setRowCount(len(headers))

        for i, h in enumerate(headers):
            self.table.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(h))

        top_headers = ('Pipe', )
        self.table.setColumnCount(len(top_headers))

        for i, h in enumerate(top_headers):
            self.table.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(h))

        self.table.horizontalHeader().setStretchLastSection(True)

        self.update_WT = True
        self.createtable()
        self.do_calcs(0, 0)
        self.table.cellChanged.connect(self.do_calcs)
        self.clip = QtGui.QApplication.clipboard()

        # self.table = QtGui.QTableWidget()
        # self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

    def comboMaterialChange(self, idx):
        if idx == len(self.materials)-1:
            # custom
            self.lineMaterialDensity.setReadOnly(False)
            self.lineMaterialModulus.setReadOnly(False)
            self.lineMaterialPoisson.setReadOnly(False)
            self.lineMaterialDensity.setStyleSheet(self.defaultBackgroundStyle)
            self.lineMaterialModulus.setStyleSheet(self.defaultBackgroundStyle)
            self.lineMaterialPoisson.setStyleSheet(self.defaultBackgroundStyle)
            # self.lineMaterialDensity.setText('')
            # self.lineMaterialModulus.setText('')
        else:
            # material from database
            self.lineMaterialDensity.setReadOnly(True)
            self.lineMaterialModulus.setReadOnly(True)
            self.lineMaterialPoisson.setReadOnly(True)
            self.lineMaterialDensity.setStyleSheet(self.readOnlyBackgroundStyle)
            self.lineMaterialModulus.setStyleSheet(self.readOnlyBackgroundStyle)
            self.lineMaterialPoisson.setStyleSheet(self.readOnlyBackgroundStyle)
            self.lineMaterialDensity.setText(str(self.materials[idx][1]))
            self.lineMaterialModulus.setText(str(self.materials[idx][2]))
            self.lineMaterialPoisson.setText(str(self.materials[idx][3]))
            self.calc_simple()

    def toggle_OD_ID_WT(self):
        """Toggles the state of the OD, ID and WT text boxes according to user selection.
        Two of them are input, and a third is calculated. User can choose which one is calculated.
        """

        if self.radioOD.isChecked():
            self.lineOD.setReadOnly(True)
            self.lineID.setReadOnly(False)
            self.lineWT.setReadOnly(False)
            self.lineOD.setStyleSheet(self.readOnlyBackgroundStyle)
            self.lineID.setStyleSheet(self.defaultBackgroundStyle)
            self.lineWT.setStyleSheet(self.defaultBackgroundStyle)
            return True
        elif self.radioID.isChecked():
            self.lineOD.setReadOnly(False)
            self.lineID.setReadOnly(True)
            self.lineWT.setReadOnly(False)
            self.lineOD.setStyleSheet(self.defaultBackgroundStyle)
            self.lineID.setStyleSheet(self.readOnlyBackgroundStyle)
            self.lineWT.setStyleSheet(self.defaultBackgroundStyle)
            return True
        elif self.radioWT.isChecked():
            self.lineOD.setReadOnly(False)
            self.lineID.setReadOnly(False)
            self.lineWT.setReadOnly(True)
            self.lineOD.setStyleSheet(self.defaultBackgroundStyle)
            self.lineID.setStyleSheet(self.defaultBackgroundStyle)
            self.lineWT.setStyleSheet(self.readOnlyBackgroundStyle)
            return True
        else:
            return False

    def calc_simple(self):
        """Every time some of the input text boxes is changed, this function is called.
        Read all inputs, check for erros, calculates properties, update output boxes.
        """

        try:
            # Reads all inputs and checks for errors
            OD = float(dot(self.lineOD.text()))                               # mm
            ID = float(dot(self.lineID.text()))                               # mm
            WT = float(dot(self.lineWT.text()))                               # mm
            E = float(dot(self.lineMaterialModulus.text()))                   # GPa, modulus
            rho = float(dot(self.lineMaterialDensity.text()))                 # kg/m3, density
            v = float(dot(self.lineMaterialPoisson.text()))                   # -, Poisson ratio
            contents_density = float(dot(self.lineContentsDensity.text()))    # kg/m3
            coating_thickness = float(dot(self.lineCoatingThickness.text()))  # mm
            coating_density = float(dot(self.lineCoatingDensity.text()))      # kg/m3
            coating2_thickness = float(dot(self.lineCoating2Thickness.text()))  # mm
            coating2_density = float(dot(self.lineCoating2Density.text()))      # kg/m3
            liner_thickness = float(dot(self.lineLinerThickness.text()))      # mm
            liner_density = float(dot(self.lineLinerDensity.text()))          # kg/m3
        except:
            self.lineAxialStiffness.setText('nan')
            self.lineBendingStiffness.setText('nan')
            self.lineTorsionalStiffness.setText('nan')
            self.lineWeightDryEmpty.setText('nan')
            self.lineWeightDryFilled.setText('nan')
            self.lineWeightWetFilled.setText('nan')
            # raise
            return False

        if self.radioWT.isChecked():
            WT = (OD-ID)/2
            self.lineWT.setText('%.4f' % WT)
        elif self.radioOD.isChecked():
            OD = ID + 2*WT
            self.lineOD.setText('%.4f' % OD)
        elif self.radioID.isChecked():
            ID = OD - 2*WT
            self.lineID.setText('%.4f' % ID)
        else:
            return False
        # Structural cross section
        EA, EI, GJ = self.cross_section(OD, ID, E, v)
        # Weights, all in kg/m
        dry_weight_empty, dry_weight_filled, wet_weight_filled = self.weights(
              OD, ID, rho, contents_density, coating_thickness, coating_density, 
              coating2_thickness, coating2_density, liner_thickness, liner_density)
        # update output
        self.lineAxialStiffness.setText('{:,.1f}'.format(EA).replace(',', ' '))
        self.lineBendingStiffness.setText('{:,.1f}'.format(EI).replace(',', ' '))
        self.lineTorsionalStiffness.setText('{:,.1f}'.format(GJ).replace(',', ' '))
        self.lineWeightDryEmpty.setText('%.3f' % dry_weight_empty)
        self.lineWeightDryFilled.setText('%.3f' % dry_weight_filled)
        self.lineWeightWetFilled.setText('%.3f' % wet_weight_filled)

    def cross_section(self, OD, ID, E, v):
        A = pi/4 * (OD**2 - ID**2)                    # mm2, cross sectional area
        I = pi/64 * (OD**4 - ID**4)                   # mm4, second moment of area
        J = 2*I                                       # mm4, second moment of area
        G = E/(2*(1+v))                               # GPa, shear modulus
        EA = E*A                                      # kN, axial stiffness
        EI = E*I/1e6                                  # kN.m2, bending stiffness
        GJ = G*J/1e6                                  # kN.m2, torsional stiffness
        return EA, EI, GJ

    def weights(self, OD, ID, rho, contents_density, coating_thickness, coating_density,
                coating2_thickness, coating2_density, liner_thickness, liner_density):
        A = pi/4 * (OD**2 - ID**2)                    # mm2, cross sectional area
        steel_weight = A*rho/1e6
        coating_weight = pi/4*((OD+2*coating_thickness)**2-(OD)**2)*coating_density/1e6
        coating2_weight = pi/4*((OD+2*(coating_thickness+coating2_thickness))**2
                                 -(OD+2*coating_thickness)**2)*coating2_density/1e6
        liner_weight = pi/4*(ID**2-(ID-2*liner_thickness)**2)*liner_density/1e6
        contents_weight = pi/4*(ID-2*liner_thickness)**2 * contents_density/1e6
        buoyancy = pi/4*(OD+2*(coating_thickness+coating2_thickness))**2 * 1025/1e6

        dry_weight_empty = steel_weight+coating_weight+coating2_weight+liner_weight
        dry_weight_filled = dry_weight_empty + contents_weight
        wet_weight_filled = dry_weight_filled - buoyancy

        return dry_weight_empty, dry_weight_filled, wet_weight_filled

    def addCol(self):
        self.table.setColumnCount(self.table.columnCount()+1)

    def delCol(self):
        self.table.setColumnCount(self.table.columnCount()-1)

    def copyCol(self):
        num_cols = self.table.columnCount()
        self.table.setColumnCount(num_cols+1)
        for i in range(self.table.rowCount()):
            self.table.setItem(i, num_cols, self.table.item(i, num_cols-1).clone())

    def cell(self, var='', locked=False):
        item = QtGui.QTableWidgetItem()
        if locked:
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setBackground(QtGui.QColor(232, 232, 232))
        item.setText(var)
        return item

    def createtable(self):
        rows = self.table.rowCount()
        columns = self.table.columnCount()
        vals = (508, 457.2, 25.4, 7850, 210, 0.293, 1000)
        locked_rows = {13, 14, 15, 16, 17, 18}
        for i in range(rows):
            for j in range(columns):
                item = self.cell(str(vals[i]) if i < len(vals) else '0.0')
                if i in locked_rows:
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, j, item)

    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            selected = self.table.selectedRanges()

            if e.key() == QtCore.Qt.Key_C:  # copy
                s = ""

                for r in range(selected[0].topRow(), selected[0].bottomRow()+1):
                    for c in range(selected[0].leftColumn(), selected[0].rightColumn()+1):
                        try:
                            s += str(self.table.item(r, c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n"  # eliminate last '\t'
                self.clip.setText(s)

    def do_calcs(self, row, col):

        if row == 2:
            # change WT - update ID
            try:
                WT = float(dot(self.table.item(2, col).text()))
                OD = float(dot(self.table.item(0, col).text()))
                ID = OD - 2*WT
                self.update_WT = False
                self.table.setItem(1, col, self.cell('%.3f' % ID))
                self.update_WT = True
                return True
            except:
                self.table.setItem(2, col, self.cell('nan'))
                self.table.setItem(13, col, self.cell('nan', True))
                self.table.setItem(14, col, self.cell('nan', True))
                self.table.setItem(15, col, self.cell('nan', True))
                self.table.setItem(16, col, self.cell('nan', True))
                self.table.setItem(17, col, self.cell('nan', True))
                self.table.setItem(18, col, self.cell('nan', True))
                return False

        if row in {0, 1, 3, 4, 5, 6, 7, 8, 9, 10}:
            try:
                OD = float(dot(self.table.item(0, col).text()))
                ID = float(dot(self.table.item(1, col).text()))
            except:
                self.table.setItem(2, col, self.cell('nan'))
                self.table.setItem(13, col, self.cell('nan', True))
                self.table.setItem(14, col, self.cell('nan', True))
                self.table.setItem(15, col, self.cell('nan', True))
                self.table.setItem(16, col, self.cell('nan', True))
                self.table.setItem(17, col, self.cell('nan', True))
                self.table.setItem(18, col, self.cell('nan', True))
                return False

            WT = (OD-ID)/2
            if self.update_WT:
                self.table.setItem(2, col, self.cell('%.3f' % WT))

            h = 'Pipe %.0fin x %.1fmm' % (OD/25.4, WT)
            self.table.setHorizontalHeaderItem(col, QtGui.QTableWidgetItem(h))
            self.table.resizeColumnsToContents()

            try:
                rho = float(dot(self.table.item(3, col).text()))
                E = float(dot(self.table.item(4, col).text()))
                v = float(dot(self.table.item(5, col).text()))
            except:
                self.table.setItem(13, col, self.cell('nan', True))
                self.table.setItem(14, col, self.cell('nan', True))
                self.table.setItem(15, col, self.cell('nan', True))
                self.table.setItem(16, col, self.cell('nan', True))
                self.table.setItem(17, col, self.cell('nan', True))
                self.table.setItem(18, col, self.cell('nan', True))
                return False

            EA, EI, GJ = self.cross_section(OD, ID, E, v)

            self.table.setItem(13, col, self.cell('{:,.1f}'.format(EA).replace(',', ' '), True))
            self.table.setItem(14, col, self.cell('{:,.1f}'.format(EI).replace(',', ' '), True))
            self.table.setItem(15, col, self.cell('{:,.1f}'.format(GJ).replace(',', ' '), True))

            try:
                contents_density = float(dot(self.table.item(6, col).text()))    # kg/m3
                coating_thickness = float(dot(self.table.item(7, col).text()))   # mm
                coating_density = float(dot(self.table.item(8, col).text()))     # kg/m3
                coating2_thickness = float(dot(self.table.item(9, col).text()))   # mm
                coating2_density = float(dot(self.table.item(10, col).text()))     # kg/m3
                liner_thickness = float(dot(self.table.item(11, col).text()))     # mm
                liner_density = float(dot(self.table.item(12, col).text()))      # kg/m3
            except:
                self.table.setItem(16, col, self.cell('nan', True))
                self.table.setItem(17, col, self.cell('nan', True))
                self.table.setItem(18, col, self.cell('nan', True))
                return False

            dry_weight_empty, dry_weight_filled, wet_weight_filled = self.weights(
                        OD, ID, rho, contents_density, coating_thickness, coating_density,
                        coating2_thickness, coating2_density, liner_thickness, liner_density)
            self.table.setItem(16, col, self.cell('%.3f' % dry_weight_empty, True))
            self.table.setItem(17, col, self.cell('%.3f' % dry_weight_filled, True))
            self.table.setItem(18, col, self.cell('%.3f' % wet_weight_filled, True))

            return True


def dot(var):
        """Replaces comma with dot in a string."""
        return var.replace(',', '.')


if __name__ == "__main__":

    # this crap below is required to get icon in windows taskbar...
    try:
        import ctypes
        myappid = u'raf.pipeproperties'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass  # ... and still need to work on other platforms.

    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
