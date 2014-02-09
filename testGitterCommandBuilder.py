import unittest
from .guiterCommandBuilder import *


class TestGiterCommandBuilder(unittest.TestCase):

    def setUp(self):
        self.path = "g8"
        self.templateName = "template/main"
        self.params = [("p1", "v1"), ("p2", "v2")]
        self.g8Command = GiterCommandBuilder(
            self.path, self.templateName, self.params)

    def test_buildGiterCommand(self):
        command = self.g8Command.buildGiterCommand()
        self.assertEqual(
            command, ["g8", "template/main", "--p1=v1", "--p2=v2"])
