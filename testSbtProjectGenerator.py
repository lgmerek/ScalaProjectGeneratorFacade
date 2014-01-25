import unittest
import subprocess


class TestSbtProjectGeneratorCommand(unittest.TestCase):

    def testfindCommandPath(self):
        output = subprocess.check_output(["which", "g8"])
        print(output.decode("utf-8"))
