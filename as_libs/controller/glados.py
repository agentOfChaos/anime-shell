import os
from PyQt4 import QtGui, QtCore

from as_libs.controller import audiovoice, shellworks
from as_libs.voicecommands import filter
import ansi2html, re


ansi_escape = re.compile(r'\x1b[^m]*m')


class CustomThread(QtCore.QThread):
    def __init__(self):
        super(CustomThread, self).__init__()
        self.busy = False

    def run(self, *args, **kwargs):
        self.busy = True
        self.target(self, *args, **kwargs)
        self.busy = False

    def __del__(self):
        self.wait()

    def output(self, data):
        self.emit(QtCore.SIGNAL("output"), data)

    def statusMessage(self, message):
        self.emit(QtCore.SIGNAL("status"), message)


class Controller(QtCore.QObject):

    def __init__(self, window, language=audiovoice.languages["italian"]):
        QtCore.QObject.__init__(self)
        self.window = window
        self.filter = filter.CommandFilter(language)
        self.audiotron = audiovoice.Audiotron()
        self.language = language

        self.audio_worker = CustomThread()
        self.connect(self.audio_worker, QtCore.SIGNAL("output"), self.processAcquiredVoice)
        self.connect(self.audio_worker, QtCore.SIGNAL("status"), self.statusMessage)


    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value
        self.filter.language = value
        self.audiotron.language = value

    def statusMessage(self, message):
        self.window.statusBar().showMessage(message)

    def acquire_voice(self):
        if not self.audio_worker.busy:
            def capsule(thread):
                thread.statusMessage("Acquiring audio...")
                data = self.audiotron.acquire()
                thread.statusMessage("Ready")
                if data is not None:
                    thread.output(data)
                else:
                    thread.statusMessage("Could not decode your audio input :(")
            self.audio_worker.target = capsule
            self.audio_worker.start()
        else:
            pass  # TODO notify?

    def calibrate_audio(self):
        if not self.audio_worker.busy:
            def capsule(thread):
                thread.statusMessage("Calibrating microphone...")
                self.audiotron.calibrate()
                thread.statusMessage("Ready")
            self.audio_worker.target = capsule
            self.audio_worker.start()
        else:
            pass  # TODO notify?

    def restart_shell(self):
        self.window.consoletext.stop()
        self.window.consoletext.execute()

    def processAcquiredVoice(self, data):
        filtered, shouldrun = self.filter.filter(data)
        print(repr(filtered))
        if shouldrun:
            filtered += "\n"
        if filtered == "panic\n":
            self.restart_shell()
        else:
            self.window.consoletext.send(bytes(filtered, "utf-8"))

    def runcommand(self, text):
        pass # TODO: rewrite