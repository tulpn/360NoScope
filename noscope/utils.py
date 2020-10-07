import json
import os
import random

import discord
from discord.ext import commands

from settings import *


def get_channel_by_name(guild, channel_name):
    """
    Get channel object by channel_name
    """
    channel = None
    for c in guild.channels:
        if c.name == channel_name.lower():
            channel = c
            break
    return channel


def get_category_by_name(guild, category_name):
    """
    Get category object by category name
    """
    category = None
    for c in guild.categories:
        if c.name == category_name:
            category = c
            break
    return category


async def notify_user(member, message):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(message)


def mods_or_owner():
    """
    Check that the user has the correct role to execute a command
    """
    def predicate(ctx):
        return commands.check_any(commands.is_owner(), commands.has_role(MODERATOR_ROLE_NAME))
    return commands.check(predicate)


def has_teaparty_role():
    """
    Check that the user has the correct role to execute a command
    This is for the telegram group chat user only!
    """
    def predicate(ctx):
        return commands.check_any(commands.has_role(TEAPARTY_ROLE_NAME))
    return commands.check(predicate)


async def get_momma_jokes():
    with open(os.path.join(DATA_DIR, "jokes.json")) as joke_file:
        jokes = json.load(joke_file)
    random_category = random.choice(list(jokes.keys()))
    insult = random.choice(list(jokes[random_category]))
    return insult


def get_games_list():
    """
    Returns a list of games 
    """
    with open(os.path.join(DATA_DIR, "games.json")) as games_file:
        games = json.load(games_file)
    return games['list']
