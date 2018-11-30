#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

https://codereview.stackexchange.com/questions/208766/capturing-stdout-in-a-qthread-and-update-gui

'''

import io
import sys
import requests
from contextlib import redirect_stdout

from PyQt5 import QtCore, QtGui, QtWidgets

out = io.StringIO()


class OutputThread(QtCore.QThread):
    
    output_changed = QtCore.pyqtSignal(object)
        
    def run(self):
        while True:
            out.flush()
            text = out.getvalue()
            if text:
                self.output_changed.emit(text)
                # clear the buffer
                out.truncate(0)
                out.seek(0)
            

class FetchDataThread(QtCore.QThread):

    # Connection between this and the main thread.
    data_fetched = QtCore.pyqtSignal(object, object)
    
    def __init__(self, url_list):
        super(FetchDataThread, self).__init__()
        self.url_list = url_list

    def update(self, url_list):
        self.url_list = url_list

    def run(self):
        
        for url in self.url_list:

            out.write('Fetching %s\n' % url)
            
            with redirect_stdout(out):
                data  = fetch_url(url)

            out.write('='*80 + '\n')
        
            # Send data back to main thread
            self.data_fetched.emit(url, data)

            
def fetch_url(url):
    '''This is a dummy function to emulate the behaviour of the module
    used in the real problem.
    
    The original module does lots of things and prints progress to stdout.
    '''
    print('Fetching', url)
    page = requests.get(url)
    print('Decoding', url)
    data  = page.content.decode()
    print('done')
    return data


class MyApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        
        # #########################################################################
        # ### GUI setup

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.button = QtWidgets.QPushButton('Go', self.centralwidget)
        self.button.clicked.connect(self.go)

        self.output_text = QtWidgets.QTextEdit()
        self.output_text.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        layout.addWidget(self.button)
        layout.addWidget(self.output_text)

        # ### end of GUI setup
        # #########################################################################

        self.url_list = ['http://www.duckduckgo.com', 'http://www.stackoverflow.com']
        self.url = list()
        self.data = list()
        
        # Thread to update text of output tab
        self.output_thread = OutputThread(self)
        self.output_thread.output_changed.connect(self.on_output_changed)
        self.output_thread.start()
        
        # Thread to fetch data
        self.fetch_data_thread = FetchDataThread(self.url_list)
        self.fetch_data_thread.data_fetched.connect(self.on_data_fetched)
        self.fetch_data_thread.finished.connect(lambda: self.button.setEnabled(True))

    def go(self):
        
        if not self.fetch_data_thread.isRunning():
            self.button.setEnabled(False)
            self.fetch_data_thread.update(self.url_list)
            self.fetch_data_thread.start()
        
    def on_data_fetched(self, url, data):
        self.url.append(url)
        self.data.append(data)
        
    def on_output_changed(self, text):
        self.output_text.append(text.strip())


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setGeometry(100, 50, 1200, 600)
    window.show()
    sys.exit(app.exec_())
