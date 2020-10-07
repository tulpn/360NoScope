# You can skip the generation of Model/Controller/Converter and Tests by supplying --bare to createcog
import logging
from .model import *

from discord import CustomActivity, Spotify

from utils import get_games_list

logger = logging.getLogger("Main")


class GamesController:
    def __init__(self):
        pass

    def list(self):
        games = get_games_list()
        return games

    def record_game(self, game):
        logger.debug(game)

        # ignore None
        if not game:
            return

        # ignore when it is custom
        if isinstance(game, CustomActivity):
            return

        # ignore anything with spotify
        if isinstance(game, Spotify):
            return

        # don't record if we already have the name
        if Game.objects(title=game.name).count() > 0:
            return
        # record new game
        g = Game()
        g.dc_id = str(game.application_id)
        g.title = game.name
        # saving game if it is unknown by name
        g.save()

    def check_if_game_ignored(self, game):
        return False
