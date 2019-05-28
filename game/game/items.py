# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import redis
import scrapy
from elasticsearch_dsl import connections

from game.models.es_types import GameType


es = connections.create_connection(hosts=["127.0.0.1"])
# redis_cli = redis.StrictRedis()
class GameItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Game(scrapy.Item):
    url = scrapy.Field()
    gameName = scrapy.Field()
    # 动作设计啥的
    gameType = scrapy.Field()
    # 开发商
    developer = scrapy.Field()
    # 发行商
    publisher = scrapy.Field()
    # 发售日期
    publishDate = scrapy.Field()
    gameLanguage = scrapy.Field()
    gameTitle = scrapy.Field()
    gamePlatform = scrapy.Field()
    # 游戏内容
    gameContext = scrapy.Field()


    def save_to_es(self):
        game = GameType()
        game.url = self["url"]
        game.developer = self["developer"]
        game.gameContext = self["gameContext"]
        game.gameLanguage = self["gameLanguage"]
        game.gameName = self["gameName"]
        game.gamePlatform = self["gamePlatform"]
        game.gameTitle = self["gameTitle"]
        game.gameType = self["gameType"]
        game.publishDate = self["publishDate"]
        game.publisher = self["publisher"]
        game.suggest = gen_suggests(GameType._index, ((game.gameName, 10),
                                                      (game.publisher, 7),
                                                      (game.gameTitle, 7),
                                                      (game.gameContext,7),
                                                      (game.developer, 7)))

        game.save()

        # redis_cli.incr("game_count")

        return


def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for (text, weight) in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index._name, body={
                "analyzer": "ik_max_word",
                "filter": ["lowercase"],
                "text": text
            })
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests