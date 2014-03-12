from .utils import Utils

def buildCommand(commandName, additionalData=[]):
    if commandName == 'gitter':
        return _giterBuilder(additionalData)
    elif commandName == 'ensime':
        return _buildSbtEnsimeCommand()
    elif commandName == 'gen-sublime':
        return _buildGenSublimeCommand()


def _giterBuilder(additionalData):
    g8CommandBuilder = _GiterCommandBuilder(
        Utils.findCommandPath("g8"), additionalData[0], additionalData[1])
    return g8CommandBuilder.buildGiterCommand()


class _GiterCommandBuilder():

    def __init__(self, g8Path, templateName, templateUserProperties):
        self.g8Path = g8Path
        self.templateName = templateName
        self.templateUserProperties = templateUserProperties

    def buildGiterCommand(self):
        g8Command = []
        g8Command.append(self.g8Path)
        g8Command.append(self.templateName)
        for p in self.templateUserProperties:
            g8Command.append(self.__buildParam(p))
        return g8Command

    def __buildParam(self, p):
        param = '--' + p[0] + '=' + p[1]
        return param


def _buildSbtEnsimeCommand():
    ensimeCommand = Utils.findCommandPath('sbt') + ' "ensime generate"'
    return ensimeCommand


def _buildGenSublimeCommand():
    genSublimeCommand = Utils.findCommandPath('sbt') + ' gen-sublime'
    return genSublimeCommand
