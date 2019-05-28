
from game.items import Game
class Utils:
    @staticmethod
    def getStr(list):
        str = ""
        for each in list:
            str += each
        return str

    @staticmethod
    def getNewGame():
        game = Game()
        game["url"] = ""
        game["developer"] = ""
        game["gameContext"] = ""
        game["gameLanguage"] = ""
        game["gameName"] = ""
        game["gamePlatform"] = ""
        game["gameTitle"] = ""
        game["gameType"] = ""
        game["publishDate"] = ""
        game["publisher"] = ""
        return game