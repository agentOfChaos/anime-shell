import pty, os


class Shell:

    def __init__(self, command="/bin/bash"):
        self.command = command
        self.processfd = None

    def start(self, outputcallback):
        self.outputcallback = outputcallback
        (child_pid, fd) = pty.fork()
        if child_pid == 0:
            os.execv(self.command, [""])
        else:
            self.processfd = fd
            self.readLoop()

    def readLoop(self):
        while True:
            try:
                data = os.read(self.processfd, 1024)
                self.outputcallback(data.decode("utf-8"))
            except OSError:
                print("end of shell")
                break

    def write(self, data, encoding="ascii"):
        os.write(self.processfd, bytes(data, encoding))


