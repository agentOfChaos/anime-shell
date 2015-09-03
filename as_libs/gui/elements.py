from PyQt4 import QtGui, QtCore

from depends.pyqtermwidget import pyqterm

def menubar(obejct):
    menuB = obejct.menuBar()
    file = menuB.addMenu('&File')

    quit = QtGui.QAction(QtGui.QIcon.fromTheme("window-close"), "Quit", obejct)
    quit.setShortcut("Ctrl+Q")
    quit.setStatusTip("Quit application")
    obejct.connect(quit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))


    file.addAction(quit)


def toolbar(object):
    object.left_toolbar = QtGui.QToolBar(object)
    object.addToolBar(QtCore.Qt.RightToolBarArea, object.left_toolbar)
    object.left_toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

    speak = QtGui.QAction(QtGui.QIcon.fromTheme("audio-input-microphone"), "Speak", object)
    speak.setShortcut("Ctrl+O")
    speak.setStatusTip("Voice input!")
    object.connect(speak, QtCore.SIGNAL('triggered()'), object.controller.acquire_voice)

    abrt = QtGui.QAction(QtGui.QIcon.fromTheme("process-stop"), "Abort", object)
    abrt.setStatusTip("Abort any running operation")
    object.connect(abrt, QtCore.SIGNAL('triggered()'), object.controller.restart_shell)

    tsst = QtGui.QAction(QtGui.QIcon.fromTheme("mail-send"), "Test", object)
    object.connect(tsst, QtCore.SIGNAL('triggered()'), object.test)

    object.left_toolbar.addAction(speak)
    object.left_toolbar.addAction(abrt)
    object.left_toolbar.addAction(tsst)


def mainTextEdit(object, layout):
    object.consoletext = pyqterm.TerminalWidget(font_size=12)
    layout.addWidget(object.consoletext)
