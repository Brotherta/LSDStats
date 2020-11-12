import os
import discord

import src.database as db
import src.utils as utils
import data.messageData as messageData

from discord.ext import commands

import logging

logger = logging.getLogger('LSDStats')


class SettingsCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="salut")
    async def test(self, ctx):
        await ctx.send("Bonjour {}".format(ctx.message.author))

    @commands.command(name="init")
    @commands.is_owner()
    async def init_bot(self, ctx):
        my_channel = None
        guild = ctx.message.guild

        await guild.create_text_channel('lsd-stats-yes')

        for channel in ctx.guild.channels:
            if channel.name == 'lsd-stats-yes':
                my_channel = channel

        accept_decline = await my_channel.send(messageData.message_dict["Init"])
        utils.write_msg_react_id(accept_decline.id)

        await accept_decline.add_reaction("✅")
        await accept_decline.add_reaction("❌")


def setup(bot):
    bot.add_cog(SettingsCommands(bot))
