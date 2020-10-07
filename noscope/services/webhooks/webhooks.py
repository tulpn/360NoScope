from discord import Webhook, RequestsWebhookAdapter
import schedule
import time
import requests

from settings import *


def check_voice_connected():
    cmd = "voice_connected"
    webhook = Webhook.partial(DISCORD_WEBHOOK_ID,
                              DISCORD_WEBHOOK_TOKEN, adapter=RequestsWebhookAdapter())
    webhook.send(cmd)


def tea_party_next_gaming_night(msg):
    webhook = Webhook.partial(DISCORD_TEA_PARTY_WEBHOOK_ID,
                              DISCORD_TEA_PARTY_WEBHOOK_TOKEN, adapter=RequestsWebhookAdapter())
    webhook.send(msg)
