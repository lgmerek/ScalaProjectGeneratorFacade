import json


class SbtTemplateDataJsonDecoder:

    def __init__(self, jsonString):
        self.data = json.loads(jsonString)

    def getData(self):
        return self.data

    def getProjectTemplatesNames(self):
        return list(self.data.keys())

    def __getProjectTemplateByName(self, templateName):
        return self.data[templateName]

    def getTemplateDefaultProperties(self, templateName):
        defaultProperties = []
        template = self.__getProjectTemplateByName(templateName)
        params = template['params']
        for k, v in params.items():
            defaultProperties.append((k, v))
        return defaultProperties
