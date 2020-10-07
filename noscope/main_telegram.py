import os
import logging
from mongoengine import *

from settings import *

from services.telegram.telegram import *


logger = logging.getLogger("Main")

connect(DB_DATABASE_NAME, host=DB_HOST_NAME, username=DB_USER,
        password=DB_PASSWORD, authentication_source="admin")


# Finally run the bot
if TELEGRAM_SECRET_TOKEN != "" and TELEGRAM_SECRET_TOKEN != None:
    tb = TelegramBot()
else:
    logger.error("Please make sure you have set the Telegram Bot Token")
