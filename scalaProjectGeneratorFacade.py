import sublime
import sublime_plugin
import subprocess
import sys
import re
from array import *
from .giterCommandThread import CommandThread
from .commandBuilders import buildCommand
from .jsonDecoderBuilder import JsonDecoderBuilder
from .sbtBuildFileEditor import SbtBuildFileEditor
from .logger import LoggerFacade


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
        self.jsonDataDecoder = JsonDecoderBuilder().createJsonDecoder()
        self.sbtTemplates = [
            self.ProjectNamePrefix + t for t in
            self.jsonDataDecoder.getProjectTemplatesNames()]

    def run(self, edit):
        self.logger = LoggerFacade.getLogger()
        self.logger.debug('\n\n----- Scala Project Generator Facade has started -----\n\n')
        self.__initProjectGeneratorFacade()
        self.view.window().show_quick_panel(
            self.sbtTemplates, self.on_projectTemplateSelected)

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
        g8ProjectDirName = ''
        if prop[0] == 'name':
            g8ProjectDirName = re.sub("\s+", '-', user_input).lower()
            self.logger.debug("g8ProjectDirName %s", g8ProjectDirName)
            self.ProjectBaseDir = self.projectPath + '/' + g8ProjectDirName
        self.templateUserProps.append((prop[0], user_input))
        self.propertyIndex += 1
        if self.propertyIndex < len(self.templateDefaultProperties):
            item = self.templateDefaultProperties[self.propertyIndex]
            self.view.window().show_input_panel(
                item[0], item[1], self.on_propetySelected, None, None)
        else:
            self.propertyIndex = 0
            try:
                g8Command = buildCommand('gitter', additionalData=[
                    self.selectedTemplateName, self.templateUserProps])
                g8Thread = CommandThread(g8Command, self.projectPath, False)
                g8Thread.start()
                self.handleGiterThread(
                    g8Thread, 100, "Giter", 'Giter Template generation')
            except subprocess.CalledProcessError:
                self.logger.info("Gitter command not found")

    def handleGiterThread(self, thread, timeout, key, message, i=0, dir=1):
        if thread.is_alive():
            a = self.animate(key, message, i, dir)
            sublime.set_timeout(
                lambda: self.handleGiterThread(thread, 100, key, message, a[0], a[1]))
        else:
            self.view.set_status(key, '')
            try:
                sbtEnsimeCommand = buildCommand('ensime')
                sbtEnsimeThread = CommandThread(
                    sbtEnsimeCommand, self.ProjectBaseDir, True)
                sbtEnsimeThread.start()
                self.handleSbtEnsimeThread(
                    sbtEnsimeThread, 100, "Ensime", "Ensime confiugration")
            except subprocess.CalledProcessError:
                self.logger.info("Ensime command not found")

    def handleSbtEnsimeThread(self, thread, timeout, key, message, i=0, dir=1):
        if thread.is_alive():
            a = self.animate(key, message, i, dir)
            sublime.set_timeout(
                lambda: self.handleSbtEnsimeThread(thread, 100, key, message, a[0], a[1]))
        else:
            self.view.set_status(key, '')
            self.modifySbtBuildFile()
            genSublimeCommand = buildCommand('gen-sublime')
            genSublimeThread = CommandThread(
                genSublimeCommand, self.ProjectBaseDir, True)
            genSublimeThread.start()
            self.handleGenSublimeThread(
                genSublimeThread, 100, "GenSublime", "Gen Sublime")

    def handleGenSublimeThread(self, thread, timeout, key, message, i=0, dir=1):
        if thread.is_alive():
            a = self.animate(key, message, i, dir)
            sublime.set_timeout(
                lambda: self.handleGenSublimeThread(thread, 100, key, message, a[0], a[1]))
        else:
            self.view.set_status(key, '')
            self.sublime_command_line(
                ['-a', self.ProjectBaseDir])

    def animate(self, key, message, i, dir):
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

    def get_sublime_path(self):
        if sublime.platform() == 'osx':
            return findCommandPath('subl')
        if sublime.platform() == 'linux':
            return open('/proc/self/cmdline').read().split(chr(0))[0]
        return sys.executable

    def sublime_command_line(self, args):
        args.insert(0, self.get_sublime_path())
        return subprocess.Popen(args)

    def modifySbtBuildFile(self):
        sbtFile = open(self.ProjectBaseDir + "/build.sbt", "a")
        sbtFileEditor = SbtBuildFileEditor(sbtFile)
        sbtFileEditor.simpleTransformationBatch(
            [('sublimeExternalSourceDirectoryName', '"ext-lib-src"'), ('sublimeTransitive', 'true')])
        sbtFileEditor.transformUsingOtherKey(('sublimeExternalSourceDirectoryParent', 'baseDirectory'))
        sbtFile.close()


def findCommandPath(command):
    rawOutput = subprocess.check_output(['which', command])
    output = rawOutput.decode("utf-8")
    return output[:-1]
