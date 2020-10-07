from discord import Webhook, RequestsWebhookAdapter
import schedule
import time
import requests

DC_WEBHOOK_URL = 'https://discordapp.com/api/webhooks/742318610877382687/JpXDYKpzWNEa4jYnQ887XtYAjrLsdQYqPd1Y1bVSi6vMJd47MFUzjMjMRsaqWgUzXxoV'

DISCORD_WEBHOOK_ID = '742318610877382687'
DISCORD_WEBHOOK_TOKEN = 'JpXDYKpzWNEa4jYnQ887XtYAjrLsdQYqPd1Y1bVSi6vMJd47MFUzjMjMRsaqWgUzXxoV'


def job():
    cmd = "voice_connected"
    webhook = Webhook.partial(DISCORD_WEBHOOK_ID,
                              DISCORD_WEBHOOK_TOKEN, adapter=RequestsWebhookAdapter())
    webhook.send(cmd, username="Webhook Guy")


schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
