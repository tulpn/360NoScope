import os
import logging
from mongoengine import *

from discord.ext import commands

from settings import *
from services.telegram.telegram import *

from uncategorised_commands.loader import load_uncategorised_commands

logger = logging.getLogger("Main")

connect(DB_DATABASE_NAME, host=DB_HOST_NAME, username=DB_USER,
        password=DB_PASSWORD, authentication_source="admin")

tb = None
if TELEGRAM_SECRET_TOKEN != "" and TELEGRAM_SECRET_TOKEN != None:
    tb = TelegramBot()

bot = commands.Bot(command_prefix=DISCORD_COMMAND_PREFIX)
bot.pipeline = tb

for filename in os.listdir(COGS_FOLDER):
    # ignore module file
    if filename.endswith(".py") or filename.startswith("_"):
        continue

    # get cog module name
    cog_folder = os.path.join(COGS_FOLDER, filename)

    # make sure its folder
    if os.path.isdir(cog_folder):
        # load cog folder cog with same name as folder
        bot.load_extension(f'cogs.{filename}.{filename}')


# Load uncategorised commands
load_uncategorised_commands(bot)

# Finally run the bot
if DISCORD_BOT_TOKEN != "" and DISCORD_BOT_TOKEN != None:
    bot.run(DISCORD_BOT_TOKEN)
else:
    logger.error("Please make sure you have set the Discord Bot Token")
