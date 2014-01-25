import unittest
import subprocess
from .commandBuilders import findCommandPath


class TestCommandBuilders(unittest.TestCase):

    def testFindNonExistingCommandPath(self):
        self.assertRaises(subprocess.CalledProcessError, findCommandPath, 'foo')

    def testFindExistingCommandPath(self):
        output = findCommandPath('ls')
        assert output
