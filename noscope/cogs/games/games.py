# This is your Cog
import logging
import discord
from discord.ext import commands

from .controller import GamesController
from utils import has_teaparty_role

logger = logging.getLogger("Main")


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.controller = GamesController()

    @commands.command()
    @has_teaparty_role()
    @commands.dm_only()
    async def list(self, ctx):
        """
        Zeigt unsere Spiele an
        """

        games_list = self.controller.list()
        embed = discord.Embed(title="Unsere Spiele")
        for game_name in games_list:
            embed.add_field(
                name=f'{game_name["name"]}', value="-", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @has_teaparty_role()
    async def play(self, ctx, num: int, what: str):
        """
        Nutze: Play Anzahl Spiel -> !play 5 valorant => sendet an die Telegram Gruppe: Ares sucht 5 Spieler fuer Valorant 
        """
        telegram_message = "%s will spielen: %s und sucht: %s spieler" % (
            ctx.message.author.display_name, what, num)
        self.bot.pipeline.sendMessage(telegram_message)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Check when someone starts playing or stops playing a game
        :param before:
        :param after:
        :return:
        """

        # ignore everything that bots do
        if after.bot or before.bot:
            return

        msg = None
        if len(before.activities) < len(after.activities):

            # record activity
            self.controller.record_game(after.activities[0])

            # ignore if this is an ignored game
            if self.controller.check_if_game_ignored(after.activities[0]):
                return

            # user started something
            msg = "%s started playing %s" % (
                after.name, after.activities[0].name)
        elif len(before.activities) > len(after.activities):
            # user stopped something
            msg = "%s stopped playing %s" % (
                after.name, str(before.activities[0]))

        logger.debug(msg)


def setup(bot):
    bot.add_cog(Games(bot))
