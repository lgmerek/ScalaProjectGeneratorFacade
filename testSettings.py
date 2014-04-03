import unittest
import sublime
from .settings import SettingsManager
from .generatorFacadeExceptions import GeneratorFacadeInitializationError


class TestSettingsManager(unittest.TestCase):

    def setUp(self):
        self.settings = sublime.load_settings(
            'SbtProjectGenerator.sublime-settings')
        EXE_WRONG.getValues()[1][2]['executable_path'] = ''

    def tearDown(self):
        self.settings.set('sbt_executable_path', '')

    def test_auto_discover_correct_executable_path(self):
        sm = SettingsManager(EXE_CORRECT)
        result = sm._auto_discover_executable_path()

        self.assertEqual(len(result), 0)
        execs = EXE_CORRECT.getValues()
        for e in execs:
            self.assertTrue(e[2]['executable_path'])

    def test_auto_discover_wrong_executable_path(self):
        sm = SettingsManager(EXE_WRONG)
        result = sm._auto_discover_executable_path()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'SBT')
        execs = EXE_WRONG.getValues()
        self.assertTrue(execs[0][2]['executable_path'])
        self.assertFalse(execs[1][2]['executable_path'])

    def test_read_wrong_executable_path_from_properties(self):
        self.sbt_path = '/usr/local/bin/fooBar'
        self.settings.set('sbt_executable_path', self.sbt_path)

        sm = SettingsManager(EXE_WRONG)
        failed = sm._auto_discover_executable_path()

        self.assertRaises(GeneratorFacadeInitializationError,
                          sm._read_executable_path_from_properties, failed)

    def test_read_correct_executable_path_from_properties(self):
        self.sbt_path = '/usr/local/bin/sbt'
        self.settings.set('sbt_executable_path', self.sbt_path)

        sm = SettingsManager(EXE_WRONG)
        failed = sm._auto_discover_executable_path()
        sm._read_executable_path_from_properties(failed)

        self.assertEqual(failed[0][2]['executable_path'], '/usr/local/bin/sbt')

    def test_create_executable_paths(self):
        self.sbt_path = '/usr/local/bin/sbt'
        self.settings.set('sbt_executable_path', self.sbt_path)

        sm = SettingsManager(EXE_WRONG)
        sm.create_executable_paths()
        execs = sm.get_executables_values()

        self.assertTrue(execs[0][2]['executable_path'])
        self.assertTrue(execs[1][2]['executable_path'])
        self.assertEqual(execs[1][2]['executable_path'], '/usr/local/bin/sbt')


class EXE_CORRECT(object):

    GITER8 = ('Giter8', 'g8',
              {'sublime_settings_name': 'g8_executable_path',
               'executable_path': ''})
    SBT = ('SBT', 'sbt',
           {'sublime_settings_name': 'sbt_executable_path',
            'executable_path': ''})

    @staticmethod
    def getValues():
        return [EXE_CORRECT.GITER8, EXE_CORRECT.SBT]


class EXE_WRONG(object):

    GITER8 = ('Giter8', 'g8',
              {'sublime_settings_name': 'g8_executable_path',
               'executable_path': ''})
    SBT = ('SBT', 'fooBar',
           {'sublime_settings_name': 'sbt_executable_path',
            'executable_path': ''})

    @staticmethod
    def getValues():
        return [EXE_WRONG.GITER8, EXE_WRONG.SBT]
