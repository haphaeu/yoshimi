# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:55:19 2017

@author: rarossi
"""

import sys
import math
from PyQt5 import QtGui, QtCore, QtWidgets
from itertools import product as iter_product
from itertools import cycle as iter_cycle
#import confidence_interval_bootstrap as cib

from results_visualiser_ui_qt5 import Ui_MainWindow
from results_loader import ResultsLoader
from results_table_qt5 import ResultsTable
_debug = True

class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Results Visualiser for Probabilistic Lifting Analysis')

        self.results = ResultsLoader()
        self.isReady2Plot = False

        self.ax = self.mpl.canvas.fig.add_subplot(111)

        self.listHs.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listTp.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listHeading.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # connect the signals with the slots
        self.actionOpen.triggered.connect(self.open_file)
        self.actionExit.triggered.connect(self.close)
        self.actionCopy.triggered.connect(self.copy)
        self.actionView_data.triggered.connect(self.openResultsTable)
        self.actionHelp.triggered.connect(self.help)
        self.actionAbout.triggered.connect(self.about)

        self.comboBox.currentIndexChanged.connect(self.selectionChangedVariable)
        self.listHs.itemSelectionChanged.connect(self.selectionChangedHs)

        self.listTp.itemSelectionChanged.connect(self.check_state)
        self.listHeading.itemSelectionChanged.connect(self.check_state)
        self.radio_log.toggled.connect(self.check_state)
        self.radio_linear.toggled.connect(self.check_state)
        self.radio_min.toggled.connect(self.check_state)
        self.radio_max.toggled.connect(self.check_state)
        self.radio_nofit.toggled.connect(self.check_state)
        self.radio_mle.toggled.connect(self.check_state)
        self.radio_me.toggled.connect(self.check_state)
        self.radio_lstsqr.toggled.connect(self.check_state)
        self.checkBoxLegend.toggled.connect(self.check_state)
        self.checkBoxCI.toggled.connect(self.check_state)
        self.checkBoxErr.toggled.connect(self.check_state)
        self.checkBoxP90.toggled.connect(self.check_state)

        self.lineEdit_level.editingFinished.connect(self.validate_ci_level)
        self.lineEdit_level.setText('0.95')
        self.ci_level = 0.95

        self.fname = None
        self.resultsTable = None

    def resizeEvent(self, event):
        if _debug: print('resize event called - w=', self.width(), 'h=', self.height())
        self.adjust_n_draw_canvas()

    def open_file(self):
        if _debug: print('open_file called')
        self.statusbar.clearMessage()
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'OpenFile')[0]
        if _debug: print('selected file ', fname)
        if not fname:
            return
        err = self.results.load(fname)

        if _debug: print('clearing lists')
        self.fname = None
        self.listHs.clear()
        self.listTp.clear()
        self.listHeading.clear()
        self.comboBox.clear()

        if err:
            self.showDialogLoadError(err)
            return
        if _debug: print('filling lists')
        self.fname = fname
        self.listHs.addItems(self.results.get_hs_list())
        self.listHs.setCurrentRow(0)
        self.listHeading.addItems(self.results.get_wd_list())
        self.listHeading.setCurrentRow(0)
        self.comboBox.addItems(self.results.get_vars())

        self.statusbar.showMessage("Sample size: %d   -   Loaded file: %s" % (self.results.seeds, fname))

    def openResultsTable(self):
        if _debug: print('openResultsTable called')
        if not self.fname == None:
            self.resultsTable = ResultsTable()
            self.resultsTable.setGeometry(600, 50, 600, 480)
            self.resultsTable.open_file(self.fname)
            self.resultsTableUpdate()
            self.resultsTable.show()

    def resultsTableUpdate(self):
        if not self.resultsTable == None:
            # filter_dict = {'WaveHs': [list...],
            #                 'WaveTp': [list...],
            #              ...}
            filter_dict = {'WaveHs': [float(x.text()) for x in self.listHs.selectedItems()],
                           'WaveTp': [float(x.text()) for x in self.listTp.selectedItems()],
                           'WaveDirection': [float(x.text()) for x in self.listHeading.selectedItems()],
                           }
            self.resultsTable.filter(filter_dict)

    def copy(self):
        #pixmap = QtGui.QPixmap.grabWidget(self.mpl.canvas)
        pixmap = QtWidgets.QWidget.grab(self.mpl.canvas)
        app.clipboard().setPixmap(pixmap)

    def help(self):
        try:
            with open('help.txt') as pf:
                msg = pf.read()
        except:
            msg = 'help file not found'
        finally:
            QtWidgets.QMessageBox.about(self, "Results Visualiser Help", msg)

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", "TechnipFMC - Norway & Russia\nHydro Analysis Discipline\nStavanger")

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

            if not self.resultsTable == None:
                self.resultsTableUpdate()
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

    def validate_ci_level(self):
        try:
            ci = float(self.lineEdit_level.text())
        except ValueError:
            self.lineEdit_level.setText('0.95')
            ci = 0.95

        # some checks on input
        if ci > 0.99:
            ci = 0.99
            self.lineEdit_level.setText('0.99')
        elif ci < 0.01:
            ci = 0.01
            self.lineEdit_level.setText('0.01')

        if _debug:
            print('ci set to', ci)

        self.ci_level = ci
        self.check_state()


    def plot(self):
        if _debug: print('plot called')
        if not (self.isReady2Plot or self.results.isAvailable):
            if _debug: print('plot returned not ready')
            return

        msg = self.statusbar.currentMessage()
        plot_msg = 'Updating plots ... ' + (
                   'this might take a sip of coffee' if self.checkBoxCI.isChecked() else '')
        self.statusbar.showMessage(plot_msg)

        self.ax.clear()
        var = self.comboBox.currentText()
        y = list(self.results.llcdf if self.radio_log.isChecked() else self.results.cdf)

        # iq modified to match the gumbel script in rlc pack:
        # iq = ResultsLoader.closest_index(y, -math.log(-math.log(0.9)) if self.radio_log.isChecked() else 0.9)
        # not sure whether this is correct though, maybe need to change both approaches to match
        # numpy.percentile(y, 90, interpolation='linear') behaviour.
        iq = 0.9 * len(y)

        tail = 'upper'
        if self.radio_min.isChecked():
            y.reverse()
            # see note above
            # iq = len(y) - 1 - iq
            iq = len(y) * 0.1
            tail = 'lower'
        # check the fit method if needed:
        if self.radio_mle.isChecked():
            fit_method = 'MLE'
        elif self.radio_me.isChecked():
            fit_method = 'ME'
        elif self.radio_lstsqr.isChecked():
            fit_method = 'LstSqr'
        else:
            fit_method = False
        # shapes and colors for plot
        marker = plot_marker_style()
        hasData = False
        plotCounter = 0
        for hs, tp, wd in iter_product(
                          [float(x.text()) for x in self.listHs.selectedItems()],
                          [float(x.text()) for x in self.listTp.selectedItems()],
                          [float(x.text()) for x in self.listHeading.selectedItems()]):
            sample = self.results.get_sample(var, hs, tp, wd)
            if not sample.empty:
                plotCounter += 1
                hasData = True
                mark = next(marker)
                if not self.checkBoxErr.isChecked():
                    # scatter only
                    self.ax.plot(sample, y, mark, label='Hs{} Tp{} wd{}'.format(hs, tp, wd))
                else:
                    # scatter + error bars
                    err = ResultsLoader.confidence_interval(sample, ci=self.ci_level, repeat=250)
                    self.ax.errorbar(sample, y, fmt=mark, xerr=(-err[0], err[1]),
                                     ecolor='gray', label='Hs{} Tp{} wd{}'.format(hs, tp, wd))
                if self.checkBoxCI.isChecked() and self.radio_log.isChecked() and plotCounter < 4:
                    # confidence interval lines
                    self.ax.plot(*ResultsLoader.fit_ci_gumbel(sample, ci=self.ci_level, repeat=250,
                                                              tail=tail), '-'+mark[1])
                if fit_method and self.radio_log.isChecked():
                    # best fit line
                    self.ax.plot(*ResultsLoader.fit(sample, y, fit_method, tail), '-'+mark[1])

                # Show where P90 is
                if self.checkBoxP90.isChecked():
                    xp90, yp90 = sample.as_matrix()[iq], y[iq]
                    xp90t = xp90
                    yp90t = yp90 - (2 if self.radio_log.isChecked() else 0.2)
                    self.ax.annotate('P90', xy=(xp90, yp90), xytext=(xp90t, yp90t),
                                     arrowprops=dict(arrowstyle='->'))
        if hasData:
            self.adjust_n_draw_canvas()

        self.statusbar.showMessage(msg)

    def adjust_n_draw_canvas(self):
        if self.isReady2Plot:
            self.ax.get_yaxis().grid(True)
            self.ax.get_xaxis().grid(True)
            self.ax.get_xaxis().set_label_text(self.comboBox.currentText())
            ylabel = 'sf' if self.radio_min.isChecked() else 'cdf'
            if self.radio_log.isChecked(): ylabel = '-log(-log(' + ylabel + '))'
            self.ax.get_yaxis().set_label_text(ylabel)
            numitems = len(self.ax.get_legend_handles_labels()[1])
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
       msg = QtWidgets.QMessageBox()
       msg.setIcon(QtWidgets.QMessageBox.Critical)
       msg.setText("Error found during loading of file.")
       msg.setInformativeText("Check the format of the input file.")
       msg.setWindowTitle("Error")
       err_msg = ''
       for i in errors:
           err_msg += i + '\n'
       msg.setDetailedText(err_msg)
       msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
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

    # this crap below is required to get icon in windows taskbar...
    try:
        import ctypes
        myappid = u'raf.resultsvisualiser'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass  # ... and still need to work on other platforms.

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    window = Window()
    window.show()
    sys.exit(app.exec_())
