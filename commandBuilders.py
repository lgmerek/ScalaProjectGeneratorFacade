import subprocess
import os


def buildCommand(commandName, additionalData=[]):
    if commandName == 'gitter':
        return _giterBuilder(additionalData)
    elif commandName == 'ensime':
        return _buildSbtEnsimeCommand()
    elif commandName == 'gen-sublime':
        return _buildGenSublimeCommand()


def _giterBuilder(additionalData):
    g8CommandBuilder = _GiterCommandBuilder(
        findCommandPath("g8"), additionalData[0], additionalData[1])
    return g8CommandBuilder.buildGiterCommand()


class _GiterCommandBuilder():

    def __init__(self, g8Path, templateName, templateUserProperites):
        self.g8Path = g8Path
        self.templateName = templateName
        self.templateUserProperites = templateUserProperites

    def buildGiterCommand(self):
        g8Command = []
        g8Command.append(self.g8Path)
        g8Command.append(self.templateName)
        for p in self.templateUserProperites:
            g8Command.append(self.__buildParam(p))
        return g8Command

    def __buildParam(self, p):
        param = "--" + p[0] + "=" + p[1]
        return param


def _buildSbtEnsimeCommand():
    ensimeCommand = findCommandPath('sbt') + ' "ensime generate"'
    return ensimeCommand


def _buildGenSublimeCommand():
    genSublimeCommand = findCommandPath('sbt') + ' gen-sublime'
    return genSublimeCommand


def findCommandPath(command):
    rawOutput = subprocess.check_output(['which', command])
    output = rawOutput.decode("utf-8")
    return output[:-1]
