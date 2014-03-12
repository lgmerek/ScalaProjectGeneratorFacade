import subprocess
import sublime
import sys


class Utils(object):

    @staticmethod
    def findCommandPath(command):
        rawOutput = subprocess.check_output(['which', command])
        output = rawOutput.decode("utf-8")
        return output[:-1]

    @staticmethod
    def get_sublime_path():
        if sublime.platform() == 'osx':
            return Utils.findCommandPath('subl')
        if sublime.platform() == 'linux':
            return open('/proc/self/cmdline').read().split(chr(0))[0]
        return sys.executable

    @staticmethod
    def execute_on_sublime_command_line(args):
        args.insert(0, Utils.get_sublime_path())
        return subprocess.Popen(args)
