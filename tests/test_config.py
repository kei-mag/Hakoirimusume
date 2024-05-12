import os
from unittest import TestCase

from hakoirimusume.config import config


class TestConfig(TestCase):

    def test_get(self):
        self.assertEqual(config.get("os.environ.path"), os.environ["PATH"])
        self.assertTrue(isinstance(config.get("hakoirimusume.aikotoba.sheeds"), list))
        self.assertEqual(config.get("hakoirimusume.alert.condition.pressure"), None)


# print(config.get("hakoirimusume.aikotoba.sheeds"))
