# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:55:19 2017

@author: rarossi
"""

import sys
import math
from PyQt4 import QtGui, QtCore
from itertools import product as iter_product
from itertools import cycle as iter_cycle

from results_visualiser_ui import Ui_MainWindow
from results_loader import ResultsLoader

_debug = True

class Window(QtGui.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.results = ResultsLoader()
        self.isReady2Plot = False

        self.ax = self.mpl.canvas.fig.add_subplot(111)

        self.listHs.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listTp.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listHeading.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        # connect the signals with the slots
        self.comboBox.currentIndexChanged .connect(self.selectionChangedVariable)
        self.actionOpen.triggered.connect(self.open_file)
        self.listHs.itemSelectionChanged.connect(self.selectionChangedHs)
        self.listTp.itemSelectionChanged.connect(self.check_state)
        self.listHeading.itemSelectionChanged.connect(self.check_state)
        self.radio_log.toggled.connect(self.check_state)
        self.radio_linear.toggled.connect(self.check_state)
        self.radio_min.toggled.connect(self.check_state)
        self.radio_max.toggled.connect(self.check_state)
        self.checkBoxLegend.toggled.connect(self.check_state)
        self.checkBoxFit.toggled.connect(self.check_state)

    def resizeEvent(self, event):
        if _debug: print('resize event called - w=', self.width(), 'h=', self.height())
        self.adjust_n_draw_canvas()

    def open_file(self):
        if _debug: print('open_file called')
        fname = QtGui.QFileDialog.getOpenFileName(self, 'OpenFile')
        err = self.results.load(fname)

        if _debug: print('clearing lists')
        self.listHs.clear()
        self.listTp.clear()
        self.listHeading.clear()
        self.comboBox.clear()
        
        if err:
            self.showDialogLoadError(err)
            return
        if _debug: print('filling lists')
        self.listHs.addItems(self.results.get_hs_list())
        self.listHs.setCurrentRow(0)
        self.listHeading.addItems(self.results.get_wd_list())
        self.listHeading.setCurrentRow(0)
        self.comboBox.addItems(self.results.get_vars())

    def check_state(self):
        if _debug: print('check_state called')
        self.isReady2Plot = False
        if ((len(list(self.listHs.selectedItems())) > 0) &
            (len(list(self.listTp.selectedItems())) > 0) &
            (len(list(self.listHeading.selectedItems())) > 0) &
            (self.comboBox.count() > 0)):
            self.isReady2Plot = True
            if _debug: print('   state ready2plot')
            self.plot()
        else:
            if _debug: print('   state not ready2plot')

    def selectionChangedHs(self):
        if _debug: print('selectionChangedHs called')
        self.listTp.clear()
        self.listTp.addItems(self.results.get_tp_list(
                             [x.text() for x in self.listHs.selectedItems()]))
        self.listTp.setCurrentRow(0)
        self.check_state()

    def selectionChangedVariable(self):
        if _debug: print('selectionChangedVariable called')
        var = self.comboBox.currentText()
        if 'max' in var.lower():
            self.radio_max.setChecked(True)
        elif 'min' in var.lower():
            self.radio_min.setChecked(True)
        self.check_state()

    def plot(self):
        if _debug: print('plot called')
        if not (self.isReady2Plot or self.results.isAvailable):
            if _debug: print('plot returned not ready')
            return
        self.ax.clear()
        var = self.comboBox.currentText()
        y = list(self.results.llcdf if self.radio_log.isChecked() else self.results.cdf)
        if self.radio_min.isChecked():
            y.reverse()
        # shapes and colors for plot
        marker = plot_marker_style()
        hasData = False
        for hs, tp, wd in iter_product(
                          [float(x.text()) for x in self.listHs.selectedItems()],
                          [float(x.text()) for x in self.listTp.selectedItems()],
                          [float(x.text()) for x in self.listHeading.selectedItems()]):
            sample = self.results.get_sample(var, hs, tp, wd)
            if not sample.empty:
                hasData = True
                mark = next(marker)
                self.ax.plot(sample, y, mark, label='Hs{} Tp{} wd{}'.format(hs, tp, wd))
                if self.checkBoxFit.isChecked() and self.radio_log.isChecked():
                    self.ax.plot(*ResultsLoader.fit(sample, y), '-'+mark[1])
        if hasData:
            self.adjust_n_draw_canvas()

    def adjust_n_draw_canvas(self):
            self.ax.get_yaxis().grid(True)
            self.ax.get_xaxis().grid(True)
            numitems = len(list(self.ax._get_legend_handles()))
            pad_top = 1
            if numitems and self.checkBoxLegend.isChecked(): 
                # trying to adjust the size of the legend and the plot to something reasonable
                ncols = math.ceil(self.mpl.canvas.width()/150)  # 150 px assumed size of one label
                nrows = math.ceil(numitems/ncols)
                pad_top = max(0.6, 1.0 - 0.025 * nrows)  # pad at top to leave room for legend
                #print('ncols', ncols, 'nrows', nrows, 'pad top', pad_top)
                self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, borderaxespad=0,
                               mode='expand', ncol=ncols, prop={'size': 8})
            self.mpl.canvas.fig.tight_layout(rect=(0, 0, 1, pad_top))  # left, bottom, right, top
            self.mpl.canvas.draw()

    def showDialogLoadError(self, errors):
       msg = QtGui.QMessageBox()
       msg.setIcon(QtGui.QMessageBox.Critical)
       msg.setText("Error found during loading of file.")
       msg.setInformativeText("Check the format of the input file.")
       msg.setWindowTitle("Error")
       err_msg = ''
       for i in errors:
           err_msg += i + '\n'
       msg.setDetailedText(err_msg)
       msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
       retval = msg.exec_()

def plot_marker_style():
        # shapes and colors for plot
        colors = 'bgrcmyk'
        shapes = 'ov^<>12348sp*hH+xDd|_'
        marker = iter_cycle(iter_product(shapes, colors))
        while True:
            cur = '%c%c' % next(marker)
            if _debug: print('generator marker: ', cur)
            yield cur

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
