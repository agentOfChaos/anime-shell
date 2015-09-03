#!/bin/python

import sys
import os
from PyQt4 import QtGui, QtCore

from as_libs import cliparse
from as_libs.gui import elements
from as_libs.controller import glados


class MainWindow(QtGui.QMainWindow):
    def __init__(self, cliargs, title="Anime-Shell"):
        QtGui.QMainWindow.__init__(self)
        self.cliargs = cliargs
        self.mainwidget = QtGui.QWidget(self)
        self.controller = glados.Controller(self)
        self.resize(800, 550)
        self.setWindowTitle(title)
        self.setupLayout()
        self.setCentralWidget(self.mainwidget)
        self.statusBar().show()
        self.initGears()

    def initGears(self):
        self.controller.calibrate_audio()

    def setupLayout(self):
        self.lvl1_horiz = QtGui.QHBoxLayout()
        self.mainwidget.setLayout(self.lvl1_horiz)
        elements.menubar(self)
        elements.toolbar(self)
        elements.mainTextEdit(self, self.lvl1_horiz)

    def test(self):
        self.consoletext.send("ls -l\n")


def main(commandline):
    app = QtGui.QApplication(sys.argv)
    main = MainWindow(commandline)
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    commandline = cliparse.parsecli()
    main(commandline)