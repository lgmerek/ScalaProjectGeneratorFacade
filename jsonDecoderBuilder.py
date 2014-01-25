import os
from .logger import LoggerFacade
from .sbtTemplateDataJsonDecoder import SbtTemplateDataJsonDecoder


class JsonDecoderBuilder:

    def __init__(self):
        self.logger = LoggerFacade.getLogger()

    def __readJsonDataFromFile(self, jsonFile):
        with open(jsonFile, "r") as jsonFile:
            return jsonFile.read().replace('\n', ' ')

    def createJsonDecoder(self):
        self.logger.debug("Json Decoder creation")
        self.logger.debug("Current Working Directory %s", os.getcwd())
        jsonData = self.__readJsonDataFromFile(
            "sbtTemplates.json")
        return SbtTemplateDataJsonDecoder(jsonData)
