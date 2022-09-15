import argparse
from os import environ
from unittest import TestCase
from unittest.mock import patch
from soku_configuration import Configuration


environ['ENV'] = 'test_env'
environ['INT'] = '12'
environ['LIST_ENV'] = '1,2'


class TesConfig(Configuration):
    DEFAULT: str = 'test_def'
    INT: int
    FLOAT: float = 5.5
    ENV: str
    ARG: str
    LIST_DEF: list = ['1', '2']
    LIST_ENV: list


class ConfigurationTests(TestCase):
    @patch.object(argparse.ArgumentParser, 'parse_args')
    def setUp(self, mock_method) -> None:
        mock_method.return_value = argparse.Namespace(ARG='test_arg')
        self.conf = TesConfig()

    def test_int(self):
        self.assertEqual(self.conf.INT, 12)

    def test_float(self):
        self.assertEqual(self.conf.FLOAT, 5.5)

    def test_default(self):
        self.assertEqual(self.conf.DEFAULT, 'test_def')

    def test_env(self):
        self.assertEqual(self.conf.ENV, 'test_env')

    def test_arg(self):
        self.assertEqual(self.conf.ARG, 'test_arg')

    def test_list(self):
        self.assertEqual(self.conf.LIST_DEF, ['1', '2'])
        self.assertEqual(self.conf.LIST_ENV, ['1', '2'])
