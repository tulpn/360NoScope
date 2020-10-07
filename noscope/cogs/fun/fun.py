# This is your Cog

import aiohttp

import discord
from discord.ext import commands

from .controller import FunController

from utils import get_momma_jokes


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.controller = FunController()

    @commands.command(brief="You Momma is!")
    async def insult(self, ctx, member: discord.Member = None):
        insult = await get_momma_jokes()
        if member is not None:
            await ctx.send("%s eat this: %s " % (member.name, insult))
        else:
            await ctx.send("%s, %s " % (ctx.message.author.name, insult))

    @commands.command(brief="Random picture of a meow")
    async def cat(self, ctx):
        async with ctx.channel.typing():
            embed = discord.Embed(title="Meow")
            embed.set_image(url="https://cataas.com/cat")
            embed.set_footer(text="https://cataas.com/cat")

            await ctx.send(embed=embed)

    @commands.command(brief="Random picture of a woof")
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Woof")
                    embed.set_image(url=data['url'])
                    embed.set_footer(text="http://random.dog/")

                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
