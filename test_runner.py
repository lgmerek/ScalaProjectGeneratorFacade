import sublime_plugin
from io import StringIO
import unittest

suites_prefix = 'SbtProjectGenerator.'
test_suites = ['testCommandBuilders', 'testGitterCommandBuilder',
               'testJsonDecoder', 'testSbtBuildFileEditor',
               'testSbtTemplateDataJsonDecoder', 'testSettings']


class RunTestSuite(sublime_plugin.WindowCommand):

    def run(self):
        test_output = ""

        for ts in test_suites:
            bucket = StringIO()
            suite = unittest.defaultTestLoader.loadTestsFromName(
                suites_prefix + ts)
            unittest.TextTestRunner(stream=bucket, verbosity=2).run(suite)
            test_output += bucket.getvalue()

        view = self.window.new_file()
        view.run_command("test_run", {"arg":test_output})


class TestRun(sublime_plugin.TextCommand):

    def run(self, edit, arg):
        self.view.insert(edit, 0, arg)
        self.view.set_scratch(True)
