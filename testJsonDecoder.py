import unittest
from .utils import EXECUTABLES
from .settings import SettingsManager
from .jsonDecoderBuilder import JsonDecoderBuilder


class TestJsonDecoderBuilder(unittest.TestCase):

    def testCreateJsonDecoder(self):
        settingsManager = SettingsManager(EXECUTABLES)
        builder = JsonDecoderBuilder(settingsManager)
        jsonDecoder = builder.createJsonDecoder()
        data = jsonDecoder.getData()
        assert data
