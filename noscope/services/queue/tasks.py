import json
import logging

from mongoengine import *

from settings import *
from webhooks.webhooks import check_voice_connected

_logger = logging.getLogger("Main")


def send_voice_count(data):
    """
    Send a webhook, to trigger the discord bot
    """
    check_voice_connected()


def send_telegram_message(msg):
    pass
