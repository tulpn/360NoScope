# 360 No Scope Discord & Telegram Bot

This is a project designed to help communicating among some gaming friends.

In a nutshell, we have a discord bot and a telegram group. I had decided to
observe activities on discord and allow certain commands to a special group.

Capabilities:

- When a player joins the "Looking for play" channel the bot sends a message to telegram and let everyone know
- From telegram you can check how many players are currently connected to voice channels
- The discord bot remembers all the games that are played from people on the discord server
- as the admin user you can load/unload/reload functionality from the bot, while the bot is running
- some random pictures of cats and dogs can be posted by the bot
- a player can query that they want to play game X and need another Y people: !play valorant 4 which will then send it to telegram
- in telegram you can vote for the next gaming night session by creating a voting poll that dynamically gets the next couple of days in case there is nothing scheduled yet
- the mandatory "yo momma" jokes are in the fun section as well !insult @username

- Can be run via Docker
- was created via create-discord-bot
- requies .env setup (see below)
- logging can be adjusted for both prod & dev
- has a global settings file, but individual settings can be overwritten by development.py and production.py files
- uses redis as a Q
- mongodb for storage

# Run instructions

Run the discord bot

```
python main.py
```

Run the telegram bot

```
python main_telegram.py
```

Or via docker:

```
docker-compose up --build
```

# .env Setup

```
DISCORD_BOT_TOKEN=


DB_HOST_NAME=
DB_DATABASE_NAME=
DB_USER=
DB_PASSWORD=


DISCORD_LOOKING_TOPLAY_CHANNEL_ID=
DISCORD_TEAPARTY_ROLE_NAME=

DISCORD_WEBHOOK_ID=
DISCORD_WEBHOOK_TOKEN=


DISCORD_TEA_PARTY_WEBHOOK_ID=
DISCORD_TEA_PARTY_WEBHOOK_TOKEN=

TELEGRAM_SECRET_TOKEN=
TELEGRAM_CHANNEL_ID=

REDIS_HOSTNAME=
```

**DISCORD_LOOKING_TOPLAY_CHANNEL_ID**

A voice channel that is observed by the bot. When a player joins this channel id, a message is sent to telegram

**DISCORD_TEAPARTY_ROLE_NAME**

A discord server group role, only these people on the server can use the telegram features.

**DISCORD_WEBHOOK_ID**

The communication between discord bot and the telegram bot are done via webhooks.
