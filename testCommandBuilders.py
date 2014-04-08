import unittest
from .commandBuilders import _GiterCommandBuilder


class TestCommandBuilders(unittest.TestCase):

    def testGiterCommandBuilderProperties(self):
        g8Path = "g8Path"
        templateName = 'template'
        templateProperties = [('name', 'Foo Bar Bar'), ('version', '0.0.1'), ('description', 'bar')]
        res = ['g8Path', 'template', '--name=Foo Bar Bar', '--version=0.0.1', '--description=bar']

        g8Builder = _GiterCommandBuilder(g8Path, templateName, templateProperties)
        command = g8Builder.buildGiterCommand()

        self.assertEqual(res, command)
