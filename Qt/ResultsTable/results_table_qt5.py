# -*- coding: utf-8 -*-
"""

Results Table
=============

Read results file from rlc, typically results.txt, and display in a table.

Created on 18-Jun-2018

@author: raf
"""

import sys
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

_debug = True


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        super(TableModel, self).__init__(parent)
        self._data = np.array(data.values)
        self._header = data.columns
        self.r, self.c = np.shape(self._data)

    def rowCount(self, parent=None):
        return self.r

    def columnCount(self, parent=None):
        return self.c

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return '%f' % self._data[index.row(), index.column()]
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self._header[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super(MyApp, self).__init__()
        self.table = QtWidgets.QTableView(self)
        self.table_filter = QtWidgets.QTableWidget(self)

        self.button1 = QtWidgets.QPushButton('Open...', self)
        self.button1.clicked.connect(self.open_file)

        self.button2 = QtWidgets.QPushButton('Filter ==>', self)
        self.button2.clicked.connect(self.filter)

        self.table_filter.setRowCount(1)
        self.table_filter.setColumnCount(3)
        for i, h in enumerate(['WaveHs', 'WaveTp', 'WaveDirection']):
            self.table_filter.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(h))
        self.table_filter.verticalHeader().setVisible(False)

        self.clip = QtWidgets.QApplication.clipboard()

        layout = QtWidgets.QGridLayout(self)
        # addWidget(widget, fromRow, fromColumn, rowSpan, columnSpan, Qt::Alignment alignment = 0)
        layout.addWidget(self.table, 0, 0, 1, 4)
        layout.addWidget(self.button1, 1, 0)
        layout.addWidget(self.button2, 2, 0)
        layout.addWidget(self.table_filter, 1, 1, 2, 3)

        self._data = []
        self._filtered_data = []

    def open_file(self):
        if _debug: print('open_file called')
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'OpenFile')[0]

        if not fname:
            return

        if _debug: print('fname', fname)
        self.load_results(fname)
        self.populate_table()

    def load_results(self, fname):
        if _debug: print('load_results called')
        # Load headers
        self._data = pd.read_table(fname)
        self._filtered_data = self._data
        return True

    def filter(self):
        if _debug: print('filter called')

        self._filtered_data = self._data
        try:
            hs = float(dot(self.table_filter.item(0, 0).text()))
        except (ValueError, AttributeError):
            hs = 0
        try:
            tp = float(dot(self.table_filter.item(0, 1).text()))
        except (ValueError, AttributeError):
            tp = 0
        try:
            wd = float(dot(self.table_filter.item(0, 2).text()))
        except (ValueError, AttributeError):
            wd = 0

        if hs:
            self._filtered_data = self._filtered_data[self._filtered_data.WaveHs == hs]
        if tp:
            self._filtered_data = self._filtered_data[self._filtered_data.WaveTp == tp]
        if wd:
            self._filtered_data = self._filtered_data[self._filtered_data.WaveDirection == wd]

        self.populate_table()

    def populate_table(self):
        if _debug: print('populate_table called')
        model = self.table.model()
        if model is not None:
            self.table.setModel(None)
            model.deleteLater()

        model = TableModel(self._filtered_data, self.table)
        self.table.setModel(model)

        return True

    def keyPressEvent(self, e):
        if _debug: print('keyPressEvent called')
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            rows, cols = list(map(list, zip(*[[i.row(), i.column()]
                              for i in self.table.selectionModel().selectedIndexes()])))
            if _debug:
                print('rows', rows)
                print('cols', cols)
            if e.key() == QtCore.Qt.Key_C:  # copy
                s = ""
                model = self.table.model()
                for row in range(min(rows), max(rows)+1):
                    for column in range(min(cols), max(cols)+1):
                        index = model.index(row, column)
                        s += model.data(index)
                        if column < max(cols):
                            s += '\t'
                    s += '\n'

                if _debug: print(s)
                self.clip.setText(s)


def dot(var):
        """Replaces comma with dot in a string."""
        return var.replace(',', '.')


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setGeometry(600, 50, 600, 480)
    window.show()
    window.open_file()
    sys.exit(app.exec_())
