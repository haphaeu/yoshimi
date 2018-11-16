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
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


class MyApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(self)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        #self.menubar.setObjectName(_fromUtf8("menubar"))
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        #self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.setStatusBar(self.statusbar)

        # Input options for the left menu:
        self.label_maker = QtWidgets.QLabel('Maker', self.centralwidget)
        self.list_maker = QtWidgets.QListWidget(self.centralwidget)
        self.list_maker.itemSelectionChanged.connect(self.maker_selection_changed)
        self.label_model = QtWidgets.QLabel('Model', self.centralwidget)
        self.list_model= QtWidgets.QListWidget(self.centralwidget)
        self.label_fuel = QtWidgets.QLabel('Fuel', self.centralwidget)
        self.list_fuel = QtWidgets.QListWidget(self.centralwidget)
        self.label_kar = QtWidgets.QLabel('Karosseri', self.centralwidget)
        self.list_kar = QtWidgets.QListWidget(self.centralwidget)
        
        self.button_add = QtWidgets.QPushButton('Add', self.centralwidget)
        self.button_add.clicked.connect(self.add_selected)
        
        self.label_selected = QtWidgets.QLabel('Selected', self.centralwidget)
        self.list_selected = QtWidgets.QListWidget(self.centralwidget)
        
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
        layout3.addWidget(self.label_kar, 2, 1, 1, 1)
        layout3.addWidget(self.list_fuel, 3, 0, 1, 1)
        layout3.addWidget(self.list_kar, 3, 1, 1, 1)
        layout3.setRowStretch(1, 2)
        layout3.setRowStretch(3, 1)
        
        layout2 = QtWidgets.QVBoxLayout()
        layout2.addLayout(layout3, stretch=10)
        layout2.addWidget(self.button_add)
        layout2.addWidget(self.label_selected)
        layout2.addWidget(self.list_selected, stretch=1)
        layout2.addWidget(self.button_get)
        
        layout1 = QtWidgets.QHBoxLayout(self.centralwidget)
        layout1.addLayout(layout2, stretch=1)
        layout1.addWidget(tabs, stretch=3)
        
        self.fill_lists()
    
    def fill_lists(self):
        mm = car_price_finn.makers_and_models
        items = ['{} [{}]'.format(x, mm[x]['count']) for x in mm]
        self.list_maker.addItems(items)
        self.list_fuel.addItem('All')
        self.list_fuel.addItems(car_price_finn.fuel_types.keys())
        self.list_kar.addItem('All')
        self.list_kar.addItems(car_price_finn.karosseri_types.keys())
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
        selected = '; '.join((maker, model))
        
        fuel = self.list_fuel.currentItem()
        if fuel and not fuel.text() == 'All':
            selected += '; ' + fuel.text()
            
        karosseri = self.list_kar.currentItem()
        if karosseri and not karosseri.text() == 'All':
            selected += '; ' + karosseri.text()
        
        
        self.list_selected.addItem(selected)
    
    def get_selected(self):
        pass
    

if __name__ == "__main__":
    
    print('Initialising database...')
    car_price_finn.fetch_makers_and_models()
    print('Done.')

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setGeometry(600, 50, 600, 480)
    window.show()
    sys.exit(app.exec_())
