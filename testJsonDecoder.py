import unittest
from .jsonDecoderBuilder import JsonDecoderBuilder


class TestJsonDecoderBuilder(unittest.TestCase):

    def testCreateJsonDecoder(self):
        builder = JsonDecoderBuilder()
        jsonDecoder = builder.createJsonDecoder()
        data = jsonDecoder.getData()
        assert data
