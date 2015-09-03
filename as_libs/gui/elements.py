from PyQt4 import QtGui, QtCore

from as_libs.thirdparty import termwidget


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

    tsst = QtGui.QAction(QtGui.QIcon.fromTheme("mail-send"), "Test", object)
    object.connect(tsst, QtCore.SIGNAL('triggered()'), object.test)

    object.left_toolbar.addAction(speak)
    object.left_toolbar.addAction(tsst)


def mainTextEdit(object, layout):
    class BakaTerm(termwidget.TermWidget):
        def childExecCommand(self, text):
            object.controller.shell.write(text)
        def isCommandComplete(self, text):
            return len(text) > 0


    object.consoletext = BakaTerm()
    object.consoletext._browser.setStyleSheet('font-size: 11pt; font-family: DejaVu Sans Mono;')
    layout.addWidget(object.consoletext)
