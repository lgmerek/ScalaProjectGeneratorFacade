import threading
import subprocess


class CommandThread(threading.Thread):

    def __init__(self, command, path, isShellUsed):
        self.command = command
        self.path = path
        self.isShellUsed = isShellUsed
        threading.Thread.__init__(self)

    def run(self):
        subprocess.call(self.command, cwd=self.path, shell=self.isShellUsed)