import unittest
from .sbtTemplateDataJsonDecoder import *


class TestSbtTemplateDataJsonDecoder(unittest.TestCase):

    def setUp(self):
        jsonString = '{"t1Name": {"params": {"p1":"v1","p2":"v2"}},"t2Name": {"params": {"p4":"v4","p5":"v5"}}}'
        self.decoder = SbtTemplateDataJsonDecoder(jsonString)

    def testGetTemplateDefaultProperties(self):
        props = self.decoder.getTemplateDefaultProperties("t1Name")
        self.assertEqual(len(props), 2)

    def testGetProjectTemplatesNames(self):
        names = self.decoder.getProjectTemplatesNames()
        self.assertEqual(len(names), 2)
        self.assertTrue("t1Name" in names)
        self.assertTrue("t2Name" in names)
