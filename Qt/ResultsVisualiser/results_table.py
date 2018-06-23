# -*- coding: utf-8 -*-
"""

Results Table
=============

Read results file from rlc, typically results.txt, and display in a table.

Created on 18-Jun-2018

@author: raf
"""
try:
    from PyQt5 import QtCore
    from PyQt5 import QtWidgets as qt
    _qt = 5
except ImportError:
    from PyQt4 import QtGui as qt
    from PyQt4 import QtCore
    _qt = 4

import sys
import numpy as np
import pandas as pd
import itertools
import subprocess
from os import path

_debug = True


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        if _debug: print('TableModel.__init__')
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


class ResultsTable(qt.QMainWindow):  #qt.QWidget):
    def __init__(self, nseeds):
        if _debug: print('ResultsTable.__init__')
        super(ResultsTable, self).__init__()
        self.setWindowTitle('Results Table')
        self.table = qt.QTableView(self)
        self.setCentralWidget(self.table)
        self.statusbar = qt.QStatusBar()
        self.setStatusBar(self.statusbar)
        self.clip = qt.QApplication.clipboard()
        
        self._data = []
        self._filtered_data = []
        self._work_path = ''
        self.num_seeds = nseeds

        # this makes the row height a bit smaller
        verticalHeader = self.table.verticalHeader()
        if _qt == 5:
            verticalHeader.setSectionResizeMode(qt.QHeaderView.Fixed)
        else:
            verticalHeader.setResizeMode(qt.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)

        # capture double click to try and lunch orcaflex at that seed
        self.table.doubleClicked.connect(self.dblClicked)
        self.table.clicked.connect(self.clicked)
        self.isDblClicked = False

    def clicked(self, modelIndex):
        if self.isDblClicked:
            self.isDblClicked = False
            return
        
        if _debug: print('clicked called.')
        row, col = modelIndex.row(), modelIndex.column()
        if _debug: print('clicked at row', modelIndex.row(), ' and column', modelIndex.column())
        # reset_index() is needed because indexes are kept after filtering.
        hs, tp, wd = self._filtered_data.reset_index().loc[row, ['WaveHs', 'WaveTp', 'WaveDirection']]
        seed_idx = row % self.num_seeds + 1
        if _debug: print('hs', hs, '   tp', tp, '   wd', wd, '   seed', seed_idx)    
        fname = './runs/Hs%.2f_Tp%05.2f_WD%d_seed%d.yml' % (hs, tp, wd, seed_idx)
        self.statusbar.showMessage("Double click to open %s" % fname)
        
    def dblClicked(self, modelIndex):
        """When the table is double clicked, Orcaflex is open for that yml file.
        This function takes some shortcuts:
           - no error checking
           - it should do less things and have help functions
           - seed number should be row % seeds
        """
        self.isDblClicked = True
        if _debug: print('dblClicked called.')
        row, col = modelIndex.row(), modelIndex.column()
        hs, tp, wd = self._filtered_data.reset_index().loc[row, ['WaveHs', 'WaveTp', 'WaveDirection']]
        seed_idx = row % self.num_seeds + 1
        fname = self._work_path + '/runs/Hs%.2f_Tp%05.2f_WD%d_seed%d.yml' % (hs, tp, wd, seed_idx)
        self.statusbar.showMessage("Opening %s" % fname)
        if _debug: print('fname', fname)

        if path.exists(fname):
            cmd = '"C:/Program Files (x86)/Orcina/OrcaFlex/10.2/Orcaflex64.exe" "%s"' % fname
            if _debug: print('cmd', cmd)
            subprocess.Popen(cmd)
        else:
            self.statusbar.showMessage("File not found: %s" % fname)
            if _debug: print('Error: file not found:', fname)

    def open_file(self, fname=None):
        """Obsolete. Keeping here for debugging purposes."""
        if _debug: print('open_file called')

        if fname is None:
            fname = qt.QFileDialog.getOpenFileName(self, 'OpenFile')
            if _qt == 5:
                fname = fname[0]

        if _debug: print('fname', fname)
        self._work_path = path.dirname(fname)
        self.load_results(fname)
        self.populate_table()

    def load_results(self, fname):
        if _debug: print('load_results called')
        # Load headers
        self._data = pd.read_table(fname)
        self._filtered_data = self._data
        return True

    def filter(self, filter_dict):
        """
        filter_dict = {'WaveHs': [list...],
                       'WaveTp': [list...],
                       ...}
        """
        if _debug: print('filter called: ', filter_dict)

        tmp = pd.DataFrame()

        for hs, tp, wd in itertools.product(filter_dict['WaveHs'],
                                            filter_dict['WaveTp'],
                                            filter_dict['WaveDirection']):
            tmp = tmp.append(self._data[(self._data.WaveHs == hs) &
                                        (self._data.WaveTp == tp) &
                                        (self._data.WaveDirection == wd)])

        self._filtered_data = tmp
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

    app = qt.QApplication(sys.argv)
    window = ResultsTable(9999)
    window.setGeometry(600, 50, 600, 480)
    window.show()
    window.open_file()
    sys.exit(app.exec_())
