import os
from unittest import TestCase

from hakoirimusume.config import config


class TestConfig(TestCase):
    def test_get(self):
        sheeds = [
            [
                "お利口で",
                "かしこくて",
                "賢くて",
                "かわいくて",
                "可愛くて",
                "キュートで",
                "げんきで",
                "元気で",
                "人見知りで",
                "優しくて",
            ],
            [
                "ご機嫌な",
                "自立した",
                "よく食べる",
                "食欲旺盛な",
                "天才な",
                "なんでも食べる？",
                "長寿な",
                "長生きな",
                "甘えん坊な",
                "癒される",
            ],
            [
                "うさぎ",
                "ウサギ",
                "Rabbit",
                "ラビット",
                "うさちゃん",
                "うさぎちゃん",
                "箱入り娘",
                "耳の長い家族",
                "ドワーフ",
                "お姫さま",
            ],
        ]
        self.assertEqual(config.get("os.environ.path"), os.environ["PATH"])
        self.assertEqual(config.get("hakoirimusume.aikotoba.sheeds"), sheeds)
        self.assertEqual(config.get("hakoirimusume.alert.condition.pressure"), None)


# print(config.get("hakoirimusume.aikotoba.sheeds"))
