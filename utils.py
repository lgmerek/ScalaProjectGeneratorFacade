
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
