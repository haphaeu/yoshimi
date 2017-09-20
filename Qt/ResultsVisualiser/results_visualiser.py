# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:55:19 2017

@author: rarossi
"""

import sys
from PyQt4 import QtGui, QtCore
import random

from results_visualiser_ui import Ui_MainWindow
from results_loader import ResultsLoader

class Window(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.listHs.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listTp.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listHeading.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        # connect the signals with the slots
        self.actionOpen.triggered.connect(self.open_file)
        self.listHs.itemSelectionChanged.connect(self.selectionChangedHs)
        
        self.fill_dummy()
        self.plot_dummy()

    def open_file(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'OpenFile')
        self.results = ResultsLoader(fname)
        self.comboBox.clear()
        self.comboBox.addItems(self.results.get_vars())
        self.listHs.clear()
        self.listHs.addItems(self.results.get_hs_list())
        self.listHeading.clear()
        self.listHeading.addItems(self.results.get_wd_list())
        self.listTp.clear()

    def selectionChangedHs(self):
        self.listTp.clear()
        print(self.listHs.selectedItems())
        print(self.results.get_tp_list(self.listHs.selectedItems()))
        self.listTp.addItems(self.results.get_tp_list(self.listHs.selectedItems()))
       
    def fill_dummy(self):
        self.comboBox.addItems(["var1", "var2", "var3 max", "var4 min"])
        
        self.listHs.addItems(['1', '2', '3.5'])
    
    def plot_dummy(self):
        ''' plot some random stuff '''

        # create an axis
        ax = self.mpl.canvas.fig.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(*self.load_res_dummy(165), 'o')
        ax.plot(*self.load_res_dummy(180), 'o')
        ax.plot(*self.load_res_dummy(195), 'o')

        # refresh canvas
        self.mpl.canvas.fig.tight_layout()
        self.mpl.canvas.draw()
    
    def load_res_dummy(self, wd):
        import pandas as pd
        df = pd.read_table("Results.txt", sep='\t')
        sample = df[(df['WaveHs'] == 3.0) & (df['WaveTp'] == 6.0) & 
                    (df['WaveDirection'] == wd)]['Link1 Max Tension']
        return sample.sort_values(), range(len(sample))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
