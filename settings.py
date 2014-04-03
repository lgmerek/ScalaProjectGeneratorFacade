import subprocess
import sublime
import os.path
from .logger import LoggerFacade
from .generatorFacadeExceptions import GeneratorFacadeInitializationError


class SettingsManager:

    def __init__(self, executables):
        self.executables = executables
        self.logger = LoggerFacade.getLogger()
        self.settings = sublime.load_settings(
            'SbtProjectGenerator.sublime-settings')

    def create_executable_paths(self):
        self.logger.info("--- Creation of executables paths ---")
        failedExecutables = self._auto_discover_executable_path()
        if (len(failedExecutables)):
            self._read_executable_path_from_properties(failedExecutables)
        self.logger.info("--- All executables paths has been created ---")

    def get_executables_values(self):
        return self.executables.getValues()

    def get_executables(self):
        return self.executables

    def _auto_discover_executable_path(self):
        self.logger.info("Trying to auto-discover paths:")
        failed = []
        for e in self.executables.getValues():
            try:
                e[2]['executable_path'] = self._findCommandPath(e[1])
                self.logger.info("executable path has been found: %s", e[0])
            except subprocess.CalledProcessError:
                failed.append(e)
                self.logger.warning(
                    "Auto-discovery for command %s has failed", e[0])
        return failed

    def _read_executable_path_from_properties(self, failedExecutables):
        self.logger.info("Reading paths from settings file:")
        for p in failedExecutables:
            res = self.settings.get(p[2]['sublime_settings_name'])
            if os.path.isfile(res):
                p[2]['executable_path'] = res
                self.logger.info("executable path has been found: %s", p[0])
            else:
                raise GeneratorFacadeInitializationError(
                    'Generator Facade Initilization Error -> ', '')

    def _findCommandPath(self, command):
        rawOutput = subprocess.check_output(['which', command])
        output = rawOutput.decode("utf-8")
        return output[:-1]
