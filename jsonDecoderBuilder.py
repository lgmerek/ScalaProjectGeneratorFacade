from .logger import LoggerFacade
from .sbtTemplateDataJsonDecoder import SbtTemplateDataJsonDecoder
from .generatorFacadeExceptions import GeneratorFacadeInitializationError


class JsonDecoderBuilder:

    def __init__(self):
        self.logger = LoggerFacade.getLogger()

    def __readJsonDataFromFile(self, jsonFile):
        with open(jsonFile, "r") as jsonFile:
            return jsonFile.read().replace('\n', ' ')

    def createJsonDecoder(self):
        self.logger.debug("Json Decoder creation")
        try:
            jsonData = self.__readJsonDataFromFile(
                "sbtTemplatesxx.json")
        except (OSError, IOError) as e:
            raise GeneratorFacadeInitializationError('Generator Facade Initilization Error -> ', str(e))
        return SbtTemplateDataJsonDecoder(jsonData)
