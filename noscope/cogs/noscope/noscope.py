# This is your Cog
import logging
import discord
from discord.ext import commands

from .controller import NoscopeController

from settings import *

logger = logging.getLogger("Main")


class Noscope(commands.Cog):
    current_streamer_list = list()

    def __init__(self, bot):
        self.bot = bot
        self.controller = NoscopeController()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        Check when user updates voice
        :param before:
        :param after:
        :return:
        """
        # ignore everything that bots do
        if member.bot:
            return

        # ignore all updates for people we don't track
        if not self.controller.check_if_tracked_user(member.id):
            return

        username = member.display_name

        # store the user
        self.controller.record_player(member)

        if not before.channel:
            # user joined a voice channel
            message = "%s ist nun im Channel: %s" % (username, after.channel)
            logger.debug(message)
            # check if it is a special channel like "looking to play"
            # send it to telegram
            if self.controller.check_ltp_channel(after.channel):
                logger.debug("SENDING TO TELEGRAM")
                self.bot.pipeline.sendMessage(message)

        if before.channel and not after.channel:
            # user left a channel
            message = "%s left channel: %s" % (username, before.channel)
            logger.debug(message)

        if before.channel and after.channel:
            if before.channel.id != after.channel.id:
                # user changed channels
                message = "%s ist nun im Channel: %s" % (
                    username, after.channel)
                logger.debug(message)
                if self.controller.check_ltp_channel(after.channel):
                    logger.debug("SENDING TO TELEGRAM")
                    self.bot.pipeline.sendMessage(message)
            else:
                # user did something else!
                if member.voice.self_stream:
                    message = "%s started streaming" % username
                    logger.debug(message)
                    # add our new streamer to a temp in memory list
                    streamer = {
                        'id': member.id,
                        'streaming': True
                    }
                    self.current_streamer_list.append(streamer)
                else:
                    # check if this member stopped streaming
                    for index in range(len(self.current_streamer_list)):
                        m = self.current_streamer_list[index]
                        if m['id'] == member.id:
                            if m['streaming'] and not member.voice.self_stream:
                                message = "%s stopped streaming" % username
                                logger.debug(message)
                                # remove streamer from temp in memory list
                                del self.current_streamer_list[index]
                                break

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == int(DISCORD_WEBHOOK_ID) and message.channel.id == 621262287415803924 and message.content == "voice_connected":
            total_connected = 0
            for vc in message.guild.voice_channels:
                total_connected += len(vc.members)
            logger.debug(
                "Total Members connected to voice channels: %s" % total_connected)
            telegram_message = "Derzeit Online im Voice: %s" % total_connected
            self.bot.pipeline.sendMessage(telegram_message)


def setup(bot):
    bot.add_cog(Noscope(bot))
