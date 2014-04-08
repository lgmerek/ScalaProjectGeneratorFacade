import sublime
import sublime_plugin
import re
import subprocess
from array import *
from .giterCommandThread import CommandThread
from .commandBuilders import buildCommand
from .jsonDecoderBuilder import JsonDecoderBuilder
from .sbtBuildFileEditor import SbtBuildFileEditor
from .logger import LoggerFacade
from .utils import EXECUTABLES
from .settings import SettingsManager
from .generatorFacadeExceptions import GeneratorFacadeInitializationError
from functools import *


class ScalaProjectGeneratorFacadeCommand(sublime_plugin.TextCommand):

    def __init__(self, k):
        sublime_plugin.TextCommand.__init__(self, k)
        self.ProjectNamePrefix = "SBT Template: "
        self.templateDefaultProperties = []
        self.templateUserProps = []
        self.selectedTemplateName = ''
        self.projectPath = ''
        self.ProjectBaseDir = ''
        self.propertyIndex = 0

    def __initProjectGeneratorFacade(self):
        self.logger.info("Generator initialization started")
        self.settingsManager = SettingsManager(EXECUTABLES)
        self.settingsManager.create_executable_paths()
        self.jsonDataDecoder = JsonDecoderBuilder(
            self.settingsManager).createJsonDecoder()
        self.sbtTemplates = [
            self.ProjectNamePrefix + t for t in
            self.jsonDataDecoder.getProjectTemplatesNames()]

    def run(self, edit):
        LoggerFacade.clear_log_file()
        self.logger = LoggerFacade.getLogger()
        self.logger.debug(
            '\n\n----- Scala Project Generator Facade has started -----\n\n')
        try:
            self.__initProjectGeneratorFacade()
            self.view.window().show_quick_panel(
                self.sbtTemplates, self.on_projectTemplateSelected)
        except GeneratorFacadeInitializationError as e:
            self.logger.error(e.message + e.causedBy)

    def on_projectTemplateSelected(self, user_input):
        # this if is only temporary workaround for Sublime 3 Beta API problem with
        # on_done event for show_quick_panel. The current Bug is that the event method is
        # called twice. First invocation returns -1, the other one is correct.
        if user_input == -1:
            return 0
        self.selectedTemplateName = (
            self.sbtTemplates[user_input])[len(self.ProjectNamePrefix):]
        self.templateDefaultProperties = self.jsonDataDecoder.getTemplateDefaultProperties(
            self.selectedTemplateName)
        self.view.window().show_input_panel(
            "Project Path", '', self.on_projectPathEntered, None, None)

    def on_projectPathEntered(self, user_input):
        self.projectPath = user_input
        item = self.templateDefaultProperties[self.propertyIndex]
        self.view.window().show_input_panel(
            item[0], item[1], self.on_propetySelected, None, None)

    def on_propetySelected(self, user_input):
        prop = self.templateDefaultProperties[self.propertyIndex]
        if prop[0] == 'name':
            self._buildProjectBaseDir(user_input)
        self.templateUserProps.append((prop[0], user_input))
        self.propertyIndex += 1
        if self.propertyIndex < len(self.templateDefaultProperties):
            item = self.templateDefaultProperties[self.propertyIndex]
            self.view.window().show_input_panel(
                item[0], item[1], self.on_propetySelected, None, None)
        else:
            self.propertyIndex = 0
            self.gitterThread()

    def _buildProjectBaseDir(self, user_input):
        g8ProjectDirName = re.sub("\s+", '-', user_input).lower()
        self.logger.debug("g8ProjectDirName %s", g8ProjectDirName)
        self.ProjectBaseDir = self.projectPath + '/' + g8ProjectDirName

    def handleThread(self, thread, timeout, key, message, handleLiveThread, nextStep, i=0, dir=1):
        if thread.is_alive():
            handleLiveThread(key, message, partial(self.handleThread,
                                                   thread, 100, key, message, handleLiveThread, nextStep), i, dir)
        else:
            self.view.set_status(key, '')
            nextStep()

    def handleLiveThread(self, key, message, currentThread, i=0, dir=1):
        def animate(i, dir):
            before = i % 8
            after = (7) - before
            if not after:
                dir = -1
            if not before:
                dir = 1
            i += 1
            self.view.set_status(
                key, message + ' [%s=%s]' % (' ' * before, ' ' * after))
            return (i, dir)

        a = animate(i, dir)
        sublime.set_timeout(lambda: currentThread(a[0], a[1]))

    def _prepareAndRunThread(self, commandName, path, isShellUsed, statusMessage, nextStep, additionalData=[]):
        command = buildCommand(commandName,
                               self.settingsManager.get_executables(), additionalData)
        thread = CommandThread(command, path, isShellUsed)
        thread.start()
        self.handleThread(
            thread, 100, commandName, statusMessage, self.handleLiveThread, nextStep)

    def gitterThread(self):
            self._prepareAndRunThread(
                'gitter', self.projectPath, False, 'Giter Template generation',
                self.ensimeThread, additionalData=[self.selectedTemplateName, self.templateUserProps])

    def ensimeThread(self):
            self._prepareAndRunThread(
                'ensime', self.ProjectBaseDir, True, "Ensime confiugration", self.genSublimeThread)

    def genSublimeThread(self):
            self.modifySbtBuildFile()
            self._prepareAndRunThread(
                'gen-sublime', self.ProjectBaseDir, True, "Gen Sublime", self.openProject)

    def openProject(self):
        self._execute_on_sublime_command_line(
            ['-a', self.ProjectBaseDir], self.settingsManager.get_executables())

    def _execute_on_sublime_command_line(self, args, execs):
        args.insert(0, execs.SUBLIME[2]['executable_path'])
        return subprocess.Popen(args)

    def modifySbtBuildFile(self):
        sbtFile = open(self.ProjectBaseDir + "/build.sbt", "a")
        sbtFileEditor = SbtBuildFileEditor(sbtFile)

        sbtFileEditor.simpleTransformationBatch(
            [('sublimeExternalSourceDirectoryName',
                '"' + self._getSettingByKey('sublime_gen_external_source_dir') + '"'),
             ('sublimeTransitive',
              self._getSettingByKey('sublime_gen_transitiv'))])
        sbtFileEditor.transformUsingOtherKey(
            ('sublimeExternalSourceDirectoryParent',
                self._getSettingByKey('sublime_gen_extenal_source_dir_parent')))
        sbtFile.close()

    def _getSettingByKey(self, key):
        return self.settingsManager.get_setting(key)
