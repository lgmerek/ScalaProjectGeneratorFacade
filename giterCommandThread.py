import threading
import subprocess
from .logger import LoggerFacade


class CommandThread(threading.Thread):

    def __init__(self, command, path, isShellUsed):
        self.command = command
        self.logger = LoggerFacade.getLogger()
        self.path = path
        self.isShellUsed = isShellUsed
        threading.Thread.__init__(self)

    def run(self):
        self.logger.info("Thread for command \n %s \n has started", self.command)
        subprocess.call(self.command, cwd=self.path, shell=self.isShellUsed)
        self.logger.info("Thread for command \n %s \n has ended", self.command)
