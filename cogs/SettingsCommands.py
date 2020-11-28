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


    @commands.command(name="count")
    async def count(self, ctx, *args):
        user_id = None
        msg = None
        channel = None

        i = 0
        while i < len(args):

            if args[i][0] == '-':
                if args[i][1] == 'u':
                    user_id = int(args[i + 1][3:len(args[i + 1]) - 1])
                    if db.get_user_id_accepts(self.bot._init_db, user_id) is not None:
                        i += 1
                    else:
                        await ctx.send("Usage: Les stats ne peuvent se faire que sur les utilisateurs ayant accepté la collecte de leurs messages.")
                        return

                elif args[i][1] == 'c':
                    channel = int(args[i+1][2:len(args[i+1])-1])
                    i += 1

                elif args[i][1] == 'm':
                    if args[i+1][0] != "-":
                        msg = args[i+1]
                        i += 1
                    else:
                        await ctx.send("Usage: count [-m \"message\"]")
                        return

                else:
                    await ctx.send("Usage: count [-u @someone] [-m \"message\"] [-c channel]")
                    return
            i += 1

        print("Infos commandes:",user_id,channel,msg)
        dico_occ = utils.get_occ_msg(self.bot._init_db,msg,user_id,channel)
        print("Réponse:",dico_occ)
        nb_occ = dico_occ["COUNT(message)"]

        await ctx.send(" Réponse: {}".format(nb_occ))



def setup(bot):
    bot.add_cog(SettingsCommands(bot))
