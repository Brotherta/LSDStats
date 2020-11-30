import os
import discord
import random
import math

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

    @commands.command(name="strip")
    async def strip_channels(self, ctx):
        accepts_list = db.get_all_user_id_accepts(self.bot._init_db)
        random_dumb = random.randint(0, len(accepts_list)-1)
        channel = ctx.channel
        messages = await channel.history(limit=1000).flatten()
        acc = 0
        for message in messages:
            if str(message.author.id) in accepts_list:
                db.insert_message_in_table(message, self.bot._init_db)
                acc += 1
        await ctx.send("J\'ai pu lire {} de vos messages ! Vous en dites des bêtises...\nSurtout toi <@{}> !".format(acc, accepts_list[random_dumb]))


    @commands.command(name="count")
    async def count(self, ctx, *args):
        user_id = None
        msg = None
        channel = None

        i = 0
        while i < len(args):

            if args[i][0] == '-':

                # Absence d'argument
                if i+1>= len(args) or args[i+1][0] == '-':
                    await ctx.send("Absence d'argument !")
                    return

                # User
                if args[i][1] == 'u':
                    user_id = args[i+1]
                    print(user_id)
                    if user_id[:3] == "<@!" and user_id[-1] == ">":    #Vérification argument
                        user_id = int(args[i + 1][3:len(args[i + 1]) - 1])
                    else:
                        await ctx.send("Mauvais argument, usage: -u @utilisateur")
                        return
                    if db.get_user_id_accepts(self.bot._init_db, user_id) is not None:   #Vérification consentement utilisateur
                        i += 1
                    else:
                        await ctx.send("Attention ! Stats uniquement sur les personnes consentantes.")
                        return

                # Channel
                elif args[i][1] == 'c':
                    channel = args[i+1]
                    if channel[:2] == "<#" and channel[-1] == ">":
                        channel = int(args[i + 1][2:len(args[i + 1]) - 1])
                    else:
                        await ctx.send("Mauvais argument, usage: -c #nom_channel ")
                        return
                    i += 1

                # Message
                elif args[i][1] == 'm':
                    if args[i+1][0] != "-":
                        msg = args[i+1]
                        i += 1
                    else:
                        await ctx.send("Usage: count [-m \"message\"]")
                        return

                # mauvaise option
                else:
                    await ctx.send("Usage: count [-u @someone] [-m \"message\"] [-c channel]")
                    return

            # pas d'option
            else:
                await ctx.send("Usage: count [-u @someone] [-m \"message\"] [-c channel]")
                return
            i += 1

        dico_occ = utils.get_occ_msg(self.bot._init_db,msg,user_id,channel)
        nb_occ = dico_occ["COUNT(message)"]

        await ctx.send(" Réponse: {}".format(nb_occ))


    # @commands.command(name="talker")
    # async def talker(self, ctx, *args):
    #     if db.get_user_id_accepts(self.bot._init_db, ctx.message.author.id) is not None:
    #         if args[0] is not None:
    #             accepts_list = db.get_all_user_id_accepts(self.bot._init_db)
    #             channel_id = int(args[0][2:len(args[0])-1])
    #             asked_channel = None
    #             for channel in ctx.message.guild.channels:
    #                 if channel.id == channel_id:
    #                     asked_channel = channel
    #
    #             if asked_channel is None:
    #                 await ctx.send("Je ne connais pas ce channel")
    #
    #             user_id = None
    #             dict_user = {}
    #             nb_msg = 0
    #             messages = await asked_channel.history(limit=2000).flatten()
    #             for message in messages:
    #                 nb_msg += 1
    #                 user_id = message.author.id
    #                 if str(user_id) in accepts_list:
    #                     if user_id in dict_user:
    #                         dict_user[user_id] += 1
    #                     else:
    #                         dict_user[user_id] = 0
    #
    #             talker_user_id = 0
    #             current = 0
    #             for talker in dict_user.keys():
    #                 if dict_user[talker] > current:
    #                     current = dict_user[talker]
    #                     talker_user_id = talker
    #             talker_user_acc = dict_user[talker_user_id]
    #
    #             stat = math.floor(talker_user_acc/nb_msg * 100)
    #             await ctx.send("Le titre d'harceleur du channel <#{}> est attribué à : <@!{}> avec un total de {}!\n Ça représente {}% des messages du channel...".format(channel_id, talker_user_id, talker_user_acc, stat))





def setup(bot):
    bot.add_cog(SettingsCommands(bot))
