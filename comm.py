from.sbtProjectGenerator import findCommandPath


def buildCommand(commandName, additionalData=()):
    return {
        'g8' : 
    }[commandName]

def giterBuilder(additionalData):
    g8CommandBuilder = GiterCommandBuilder(
        findCommandPath("g8"), self.selectedTemplateName, self.templateUserProps)
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


def _buildSbtEnsimeCommand(self):
    ensimeCommand = findCommandPath('sbt') + ' "ensime generate"'
    return ensimeCommand


def _buildGenSublimeCommand(self):
    genSublimeCommand = findCommandPath('sbt') + ' gen-sublime'
    return genSublimeCommand
