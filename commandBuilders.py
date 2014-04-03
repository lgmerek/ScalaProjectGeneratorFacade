def buildCommand(commandName, execs, additionalData=[]):
    if commandName == 'gitter':
        return _giterBuilder(execs.GITER8, additionalData)
    elif commandName == 'ensime':
        return _buildSbtEnsimeCommand(execs.SBT)
    elif commandName == 'gen-sublime':
        return _buildGenSublimeCommand(execs.SBT)


def _giterBuilder(g8_exec, additionalData):
    g8CommandBuilder = _GiterCommandBuilder(
        g8_exec[2]['executable_path'], additionalData[0], additionalData[1])
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


def _buildSbtEnsimeCommand(sbt_exec):
    ensimeCommand = sbt_exec[2]['executable_path'] + ' "ensime generate"'
    return ensimeCommand


def _buildGenSublimeCommand(sbt_exec):
    genSublimeCommand = sbt_exec[2]['executable_path'] + ' gen-sublime'
    return genSublimeCommand
