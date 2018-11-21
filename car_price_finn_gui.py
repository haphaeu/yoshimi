#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 19:26:02 2018

@author: raf
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import car_price_finn


class MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MatplotlibWidget(QtWidgets.QWidget):
    """Widget defined in Qt Designer"""

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


class MyApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)

        # #########################################################################
        # ### GUI setup

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        # self.menubar.setObjectName(_fromUtf8("menubar"))
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        # self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.statusbar.showMessage('data source: finn.no')
        self.setStatusBar(self.statusbar)

        # Input options for the left menu:
        self.label_maker = QtWidgets.QLabel('Maker', self.centralwidget)
        self.list_maker = QtWidgets.QListWidget(self.centralwidget)
        self.list_maker.itemSelectionChanged.connect(self.maker_selection_changed)
        self.label_model = QtWidgets.QLabel('Model', self.centralwidget)
        self.list_model = QtWidgets.QListWidget(self.centralwidget)
        self.label_fuel = QtWidgets.QLabel('Fuel', self.centralwidget)
        self.list_fuel = QtWidgets.QListWidget(self.centralwidget)
        self.label_body= QtWidgets.QLabel('Body', self.centralwidget)
        self.list_body= QtWidgets.QListWidget(self.centralwidget)

        self.button_add = QtWidgets.QPushButton('Add', self.centralwidget)
        self.button_add.clicked.connect(self.add_selected)

        self.label_selected = QtWidgets.QLabel('Selected', self.centralwidget)

        # Set up the table for selected cars
        self.table_selected = QtWidgets.QTableWidget(0, 4, self.centralwidget)
        self.table_selected.horizontalHeader().setVisible(True)
        self.table_selected.verticalHeader().setVisible(False)
        self.table_selected.horizontalHeader().setStretchLastSection(False)
        self.table_selected.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        headers = ('Maker', 'Model', 'Fuel', 'Body')
        for i, h in enumerate(headers):
            self.table_selected.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(h))

        self.table_selected.horizontalHeader().setStretchLastSection(True)

        self.button_get = QtWidgets.QPushButton('Get', self.centralwidget)
        self.button_get.clicked.connect(self.get_selected)

        # Tabs on the right
        tabs = QtWidgets.QTabWidget(self.centralwidget)
        tab1 = QtWidgets.QWidget()
        tab2 = QtWidgets.QWidget()
        tab3 = QtWidgets.QWidget()
        tabs.addTab(tab1, 'Plot')
        tabs.addTab(tab2, 'Data')
        tabs.addTab(tab3, 'Output')

        # Tab1
        self.mpl = MatplotlibWidget(tab1)
        self.mpl.setGeometry(QtCore.QRect(130, 70, 561, 291))
        self.mpl.setObjectName('mpl')
        tmp_layout = QtWidgets.QHBoxLayout()
        tmp_layout.addWidget(self.mpl)
        tab1.setLayout(tmp_layout)

        # Tab2
        # TBC

        # Tab3
        # TBC

        layout3 = QtWidgets.QGridLayout()
        layout3.addWidget(self.label_maker, 0, 0, 1, 1)
        layout3.addWidget(self.label_model, 0, 1, 1, 1)
        layout3.addWidget(self.list_maker, 1, 0, 1, 1)
        layout3.addWidget(self.list_model, 1, 1, 1, 1)
        layout3.addWidget(self.label_fuel, 2, 0, 1, 1)
        layout3.addWidget(self.label_body, 2, 1, 1, 1)
        layout3.addWidget(self.list_fuel, 3, 0, 1, 1)
        layout3.addWidget(self.list_body, 3, 1, 1, 1)
        layout3.setRowStretch(1, 2)
        layout3.setRowStretch(3, 1)

        layout2 = QtWidgets.QVBoxLayout()
        layout2.addLayout(layout3, stretch=2)
        layout2.addWidget(self.button_add)
        layout2.addWidget(self.label_selected)
        layout2.addWidget(self.table_selected, stretch=1)
        layout2.addWidget(self.button_get)

        layout1 = QtWidgets.QHBoxLayout(self.centralwidget)
        layout1.addLayout(layout2, stretch=1)
        layout1.addWidget(tabs, stretch=3)

        self.fill_lists()

        # ### end of GUI setup
        # #########################################################################

        self._car_selection = list()
        self._data = dict()
        self._stats = dict()


    def fill_lists(self):
        mm = car_price_finn.makers_and_models
        items = ['{} [{}]'.format(x, mm[x]['count']) for x in mm]
        self.list_maker.addItems(items)
        self.list_fuel.addItem('All')
        self.list_fuel.addItems(car_price_finn.fuel_types.keys())
        self.list_body.addItem('All')
        self.list_body.addItems(car_price_finn.karosseri_types.keys())
        # Select first maker to fill models
        self.list_maker.setCurrentRow(0)

    def maker_selection_changed(self):
        self.list_model.clear()
        maker = self.list_maker.selectedItems()[0].text().split('[')[0].strip()
        mm = car_price_finn.makers_and_models
        items = ['{} [{}]'.format(x, mm[maker]['models'][x]['count']) for x in mm[maker]['models']]
        self.list_model.addItems(items)

    def add_selected(self):
        model = self.list_model.currentItem()
        if not model:
            return

        maker = self.list_maker.currentItem().text().split('[')[0].strip()
        model = model.text().split('[')[0].strip()

        fuel = self.list_fuel.currentItem()
        if fuel and not fuel.text() == 'All':
            fuel = fuel.text()
        else:
            fuel = None

        body = self.list_body.currentItem()
        if body and not body.text() == 'All':
            body = body.text()
        else:
            body = None

        # Check if selected car is already in the list
        car = car_price_finn.Car(maker, model, fuel, body)
        if car in self._car_selection:
            return  # do nothing

        self._car_selection.append(car)

        # Update table
        row = self.table_selected.rowCount()
        self.table_selected.setRowCount(row + 1)
        self.table_selected.setItem(row, 0, QtWidgets.QTableWidgetItem(maker))
        self.table_selected.setItem(row, 1, QtWidgets.QTableWidgetItem(model))
        self.table_selected.setItem(row, 2, QtWidgets.QTableWidgetItem(fuel))
        self.table_selected.setItem(row, 3, QtWidgets.QTableWidgetItem(body))

    def get_selected(self):
        '''
        THIS NEEDS TO GO TO A THREAD...
        see SO for example...
        '''
        
        # some dummy plotting
        self.mpl.canvas.ax.clear()
        self.mpl.canvas.ax.plot([1,2],[4,3])
        self.mpl.canvas.draw()
        
        for car in self._car_selection:

            print('\n', '='*len(car.id), '\n', car.id, '\n', '='*len(car.id), '\n')
            if car.id not in self._data:
                self._data[car.id] = car_price_finn.getalldata(car.url)
            else:
                print(car.id, 'already in the database.')

            print('Found', len(self._data[car.id]), 'entries.')
            self._stats[car.id] = car_price_finn.getstats(self._data[car.id])
            car_price_finn.print_stats(self._stats[car.id])
            print()


if __name__ == "__main__":

    print('Initialising database... ', end='')
    car_price_finn.fetch_makers_and_models()
    print('Done.')

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setGeometry(100, 50, 1200, 600)
    window.setWindowTitle('CarPrice')
    window.show()
    sys.exit(app.exec_())
