# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'results_visualiser.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 621)
        MainWindow.setMinimumSize(QtCore.QSize(800, 500))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.verticalLayout.addWidget(self.comboBox)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listHs = QtGui.QListWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listHs.sizePolicy().hasHeightForWidth())
        self.listHs.setSizePolicy(sizePolicy)
        self.listHs.setMaximumSize(QtCore.QSize(60, 16777215))
        self.listHs.setObjectName(_fromUtf8("listHs"))
        self.gridLayout.addWidget(self.listHs, 1, 0, 1, 1)
        self.listTp = QtGui.QListWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listTp.sizePolicy().hasHeightForWidth())
        self.listTp.setSizePolicy(sizePolicy)
        self.listTp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.listTp.setObjectName(_fromUtf8("listTp"))
        self.gridLayout.addWidget(self.listTp, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.listHeading = QtGui.QListWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listHeading.sizePolicy().hasHeightForWidth())
        self.listHeading.setSizePolicy(sizePolicy)
        self.listHeading.setMaximumSize(QtCore.QSize(60, 9999))
        self.listHeading.setObjectName(_fromUtf8("listHeading"))
        self.gridLayout.addWidget(self.listHeading, 1, 2, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.radio_mle = QtGui.QRadioButton(self.groupBox_3)
        self.radio_mle.setObjectName(_fromUtf8("radio_mle"))
        self.gridLayout_4.addWidget(self.radio_mle, 0, 1, 1, 1)
        self.radio_nofit = QtGui.QRadioButton(self.groupBox_3)
        self.radio_nofit.setChecked(True)
        self.radio_nofit.setObjectName(_fromUtf8("radio_nofit"))
        self.gridLayout_4.addWidget(self.radio_nofit, 0, 0, 1, 1)
        self.radio_lstsqr = QtGui.QRadioButton(self.groupBox_3)
        self.radio_lstsqr.setObjectName(_fromUtf8("radio_lstsqr"))
        self.gridLayout_4.addWidget(self.radio_lstsqr, 1, 0, 1, 1)
        self.radio_me = QtGui.QRadioButton(self.groupBox_3)
        self.radio_me.setObjectName(_fromUtf8("radio_me"))
        self.gridLayout_4.addWidget(self.radio_me, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_3, 2, 0, 1, 2)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.radio_log = QtGui.QRadioButton(self.groupBox)
        self.radio_log.setChecked(True)
        self.radio_log.setObjectName(_fromUtf8("radio_log"))
        self.buttonGroup = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.radio_log)
        self.horizontalLayout_2.addWidget(self.radio_log)
        self.radio_linear = QtGui.QRadioButton(self.groupBox)
        self.radio_linear.setObjectName(_fromUtf8("radio_linear"))
        self.buttonGroup.addButton(self.radio_linear)
        self.horizontalLayout_2.addWidget(self.radio_linear)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.radio_max = QtGui.QRadioButton(self.groupBox_2)
        self.radio_max.setChecked(True)
        self.radio_max.setObjectName(_fromUtf8("radio_max"))
        self.buttonGroup_2 = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName(_fromUtf8("buttonGroup_2"))
        self.buttonGroup_2.addButton(self.radio_max)
        self.horizontalLayout_3.addWidget(self.radio_max)
        self.radio_min = QtGui.QRadioButton(self.groupBox_2)
        self.radio_min.setObjectName(_fromUtf8("radio_min"))
        self.buttonGroup_2.addButton(self.radio_min)
        self.horizontalLayout_3.addWidget(self.radio_min)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 2)
        self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.checkBoxErr = QtGui.QCheckBox(self.groupBox_4)
        self.checkBoxErr.setObjectName(_fromUtf8("checkBoxErr"))
        self.gridLayout_3.addWidget(self.checkBoxErr, 1, 0, 1, 1)
        self.checkBoxCI = QtGui.QCheckBox(self.groupBox_4)
        self.checkBoxCI.setObjectName(_fromUtf8("checkBoxCI"))
        self.gridLayout_3.addWidget(self.checkBoxCI, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.lineEdit_level = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_level.setObjectName(_fromUtf8("lineEdit_level"))
        self.gridLayout_3.addWidget(self.lineEdit_level, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_4, 3, 0, 1, 2)
        self.checkBoxLegend = QtGui.QCheckBox(self.centralwidget)
        self.checkBoxLegend.setChecked(True)
        self.checkBoxLegend.setObjectName(_fromUtf8("checkBoxLegend"))
        self.gridLayout_2.addWidget(self.checkBoxLegend, 4, 0, 1, 1)
        self.checkBoxP90 = QtGui.QCheckBox(self.centralwidget)
        self.checkBoxP90.setObjectName(_fromUtf8("checkBoxP90"))
        self.gridLayout_2.addWidget(self.checkBoxP90, 4, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 3, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.mpl = MatplotlibWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl.sizePolicy().hasHeightForWidth())
        self.mpl.setSizePolicy(sizePolicy)
        self.mpl.setBaseSize(QtCore.QSize(0, 0))
        self.mpl.setObjectName(_fromUtf8("mpl"))
        self.horizontalLayout.addWidget(self.mpl)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName(_fromUtf8("actionHelp"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionCopy)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_2.setText(_translate("MainWindow", "Select a variable:", None))
        self.label_3.setText(_translate("MainWindow", "Tp [s]", None))
        self.label.setText(_translate("MainWindow", "Hs [m]", None))
        self.label_4.setText(_translate("MainWindow", "WDir [deg]", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Fit Model", None))
        self.radio_mle.setText(_translate("MainWindow", "MLE", None))
        self.radio_nofit.setText(_translate("MainWindow", "None", None))
        self.radio_lstsqr.setText(_translate("MainWindow", "LstSqr", None))
        self.radio_me.setText(_translate("MainWindow", "ME", None))
        self.groupBox.setTitle(_translate("MainWindow", "y axis", None))
        self.radio_log.setText(_translate("MainWindow", "log-log", None))
        self.radio_linear.setText(_translate("MainWindow", "linear", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Sample", None))
        self.radio_max.setText(_translate("MainWindow", "Maxima", None))
        self.radio_min.setText(_translate("MainWindow", "Minima", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Confidence Intervals", None))
        self.checkBoxErr.setText(_translate("MainWindow", "Quantiles", None))
        self.checkBoxCI.setText(_translate("MainWindow", "Model", None))
        self.label_5.setText(_translate("MainWindow", "Level", None))
        self.lineEdit_level.setText(_translate("MainWindow", "0.95", None))
        self.checkBoxLegend.setText(_translate("MainWindow", "Legend", None))
        self.checkBoxP90.setText(_translate("MainWindow", "P90", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionHelp.setText(_translate("MainWindow", "Help", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionCopy.setText(_translate("MainWindow", "Copy", None))
        self.actionOpen.setText(_translate("MainWindow", "Open...", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

from matplotlibwidget import MatplotlibWidget
