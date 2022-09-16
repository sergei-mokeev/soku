from unittest import TestCase
from soku_service import Service
from aiohttp.web import Application


class ObjectTests(TestCase):
    def test_sevice(self):
        s = Service()
        a = Application()
        s.set_aiohttp_app(a)
        self.assertIs(s.app, a)
