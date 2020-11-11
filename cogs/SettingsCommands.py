import os
import discord

import src.database as db

from discord.ext import commands

class SettingsCommands(commands.Cog):

    def __init__(self,bot):
        self.bot = bot


    @commands.command(name="salut")
    async def test(self, ctx):
        await ctx.send("Bonjour {}".format(ctx.message.author))

    @commands.command(name="init")
    @commands.is_owner()
    
    async def init_bot(self, ctx):
        mychannel = None
        guild = ctx.message.guild

        await guild.create_text_channel('lsd-stats-yes')

        for channel in ctx.guild.channels:
            if channel.name == 'lsd-stats-yes':
                mychannel = channel

        await mychannel.set_permissions(ctx.guild.default_role, send_messages=False)


def setup(bot):
    bot.add_cog(SettingsCommands(bot))