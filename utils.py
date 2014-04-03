import subprocess


class EXECUTABLES(object):

    GITER8 = ('Giter8', 'g8',
              {'sublime_settings_name': 'g8_executable_path',
               'executable_path': ''})
    SBT = ('SBT', 'sbt',
           {'sublime_settings_name': 'sbt_executable_path',
            'executable_path': ''})

    SUBLIME = ('SublimeText', 'subl',
               {'sublime_settings_name': 'sublime_executable_path',
                'executable_path': ''})

    @staticmethod
    def getValues():
        return [EXECUTABLES.GITER8, EXECUTABLES.SBT, EXECUTABLES.SUBLIME]


class Utils(object):

    @staticmethod
    def findCommandPath(command):
        rawOutput = subprocess.check_output(['which', command])
        output = rawOutput.decode("utf-8")
        return output[:-1]

    # commentet out until support for all executables will be investigated
    # for each platform
    #@staticmethod
    #def get_sublime_path():
    #    if sublime.platform() == 'osx':
    #        return Utils.findCommandPath('subl')
    #    if sublime.platform() == 'linux':
    #        return open('/proc/self/cmdline').read().split(chr(0))[0]
    #    return sys.executable

    @staticmethod
    def execute_on_sublime_command_line(args, execs):
        args.insert(0, execs.SUBLIME[2]['executable_path'])
        return subprocess.Popen(args)
