

class SbtBuildFileEditor:

    def __init__(self, outputHandle):
        self.outputHandle = outputHandle
        commentInfo = "\n\n// ----- This part is generated by Scala Project Generator Facade plugin -----"
        self.__writeToOutputHandle(commentInfo)

    def simpleTransformation(self, kv):
        key, value = kv
        t = '\n\n' + key + ' := ' + value
        self.__writeToOutputHandle(t)

    def simpleTransformationBatch(self, kvList):
        for t in kvList:
            self.simpleTransformation(t)

    def transformUsingOtherKey(self, kv):
        key, otherKey = kv
        t = '\n\n' + key + ' <<= ' + otherKey
        self.__writeToOutputHandle(t)

    def transformUsingOtherKeyBatch(self, kvList):
        for t in kvList:
            self.transformUsingOtherKey(t)

    def __writeToOutputHandle(self, data):
        self.outputHandle.write(data)
