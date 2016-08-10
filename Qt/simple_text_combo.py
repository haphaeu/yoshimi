"""
from:
http://zetcode.com/gui/pyqt4/

"""
import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.lbl = QtGui.QLabel("some text", self)

        # set up combo box
        combo = QtGui.QComboBox(self)
        combo.addItem("Steel")
        combo.addItem("Aluminium")
        combo.addItem("Titanium")
        combo.addItem("Concrete")
        combo.addItem("Polymer")

        combo.move(50, 50)
        self.lbl.move(50, 150)

        combo.activated[str].connect(self.onActivated)

        # set up text boxes
        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)
        self.le.textChanged.connect(self.onText)

        self.le2 = QtGui.QLineEdit(self)
        self.le2.move(130, 44)

        # set up window
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QComboBox')
        self.show()

    def onActivated(self, text):

        self.lbl.setText(text)
        self.lbl.adjustSize()

    def onText(self):
        try:
            val = str(float(self.le.text())*2)
        except:
            val = 'nan'
        self.le2.setText(val)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
