import os
import discord
import random
import math
import logging

import src.database as db
import src.utils as utils
import data.messageData as messageData

from discord.ext import commands
from random import randint

logger = logging.getLogger('LSDStats')


class SettingsCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="salut")
    async def test(self, ctx):
        embed = discord.Embed(
            title="🤖 Biboop, I love stats !",
            color=utils.COLOR
        )
        embed.add_field(
            name="👋 HELLO 👋",
            value="How are you {} ?".format(ctx.message.author),
            inline=False
        )
        await ctx.send(embed=embed)

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
        accepts_list = db.get_all_user_id_accepts(self.bot.init_db)
        random_dumb = random.randint(0, len(accepts_list) - 1)
        channel = ctx.channel
        messages = await channel.history(limit=1000).flatten()
        acc = 0
        for message in messages:
            if str(message.author.id) in accepts_list:
                db.insert_message_in_table(message, self.bot.init_db)
                acc += 1
        await ctx.send("J\'ai pu lire {} de vos messages ! "
                       "Vous en dites des bêtises...\nSurtout toi <@{}> !".format(acc, accepts_list[random_dumb]))

    @commands.command(name="count")
    async def count(self, ctx, *args):
        error_embed = discord.Embed(
            title="🤖 Biboop, I love stats ! Mayday ! There is a problem Jackson ! ☠",
            color=utils.COLOR
        )
        error_embed.add_field(
            name="Count commands !",
            value="📚 `s!count [-u @someone] [-m \"message\"] [-c #channel]`\nIsn't hard to understand right ?",
            inline=False
        )

        user_id = None
        msg = None
        channel = None
        i = 0
        while i < len(args):

            if args[i][0] == '-':
                # Absence d'argument
                if i + 1 >= len(args) or args[i + 1] == "" or args[i + 1][0] == '-':
                    await ctx.send(embed=error_embed.add_field(name='Error :', value="There is no args", inline=False))
                    return
                # User
                if args[i][1] == 'u':
                    user_id = args[i + 1]
                    if user_id[:2] == "<@" and user_id[-1] == ">":
                        # Vérification argument
                        if user_id[2] == '!':
                            user_id = int(args[i + 1][3:len(args[i + 1]) - 1])
                        else:
                            user_id = int(args[i + 1][2:len(args[i + 1]) - 1])
                    else:
                        await ctx.send(embed=error_embed)
                        return
                    if str(user_id) in self.bot.is_accepting:  # Vérification consentement utilisateur
                        i += 1
                    else:
                        await ctx.send(embed=error_embed.add_field(name='Error :', value="Not Available on papi...",
                                                                   inline=False))
                        return
                # Channel
                elif args[i][1] == 'c':
                    channel = args[i + 1]
                    if channel[:2] == "<#" and channel[-1] == ">":
                        channel = int(args[i + 1][2:len(args[i + 1]) - 1])
                    else:
                        await ctx.send(embed=error_embed)
                        return
                    i += 1
                # Message
                elif args[i][1] == 'm':
                    if args[i + 1][0] != "-":
                        msg = args[i + 1]
                        i += 1
                    else:
                        await ctx.send(embed=error_embed)
                        return
                # mauvaise option
                else:
                    await ctx.send(embed=error_embed)
                    return
            # pas d'option
            else:
                await ctx.send(embed=error_embed)
                return
            i += 1

        dico_occ = utils.get_occ_msg(self.bot.init_db, msg, user_id, channel)
        nb_occ = dico_occ["COUNT(message)"]
        embed = discord.Embed(
            title="🤖 Biboop, I love stats ! Here's my count...",
            color=utils.COLOR
        )
        embed.add_field(
            name="📈 Stats results :",
            value="There is {} messages...".format(nb_occ),
            inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name="talker")
    async def talker(self, ctx, *args):
        if len(args) == 0:
            embed = discord.Embed(
                title="🤖 Biboop, I love stats ! Mayday ! There is a problem Jackson ! ☠",
                color=utils.COLOR
            )
            embed.add_field(
                name="Talker commands !",
                value="📚 `s!talker #channel`\nGive the user who's "
                      "the most active of the server, or in a specific channel.",
                inline=False
            )
            await ctx.send(embed=embed)
        else:
            channel_id = 0
            try:
                channel_id = int(args[0][2:len(args[0]) - 1])
            except ValueError as e:
                embed = discord.Embed(
                    title="🤖 Biboop, I love stats ! But I don't know `{}` channel ! ☠".format(args[0]),
                    color=utils.COLOR
                )
                await ctx.send(embed=embed)
                logger.exception(e)

            if channel_id != 0:
                talker_dict = db.get_talker_channel(self.bot.init_db, channel_id)
                all_message = db.get_all_msg_channel(self.bot.init_db, channel_id)
                user_id = talker_dict['UserID']
                nb_msg_user = talker_dict['nb']
                nb_msg = all_message['nb']

                stat = math.floor(nb_msg_user / nb_msg * 100)
                embed = discord.Embed(
                    title="🤖 Biboop, I love stats ! Here's my count...",
                    color=utils.COLOR
                )
                embed.add_field(
                    name="📈 Stats results :",
                    value="The title of <#{}>'s channel harasser is attributed to : <@!{}> With `{}` messages!\n "
                          "It's `{}%` of total messages...".format(channel_id, user_id, nb_msg_user, stat),
                    inline=False
                )
                await ctx.send(embed=embed)

    @commands.command(name="quote")
    async def quote(self, ctx, *args):
        error_embed = discord.Embed(
            title="🤖 Biboop, I love stats ! Mayday ! There is a problem Jackson ! ☠",
            color=utils.COLOR
        )
        error_embed.add_field(
            name="Quote commands !",
            value="📚 `s!quote [#channel]`\nGive a sentence or a word out of his context\n\n\n\n",
            inline=False
        )
        if len(args) == 0:
            res = db.get_all_message_id(self.bot.init_db, 0, 20)
        else:
            channel_id = utils.channel_to_channel_id(args[0])
            if channel_id == 0:
                await ctx.send(embed=error_embed)
                return
            else:
                res = db.get_all_message_id(self.bot.init_db, channel_id, 20)
                if len(res) == 0:
                    print("yes wrong")
                    await ctx.send(embed=discord.Embed(
                        title="🤖 Biboop, I love stats ! Mayday ! There is a problem Jackson ! ☠",
                        color=utils.COLOR
                    ).add_field(
                        name="Quote commands !",
                        value="📚 `s!quote [#channel]`\nThere is no message with {} char or more".fomrat(20),
                        inline=False
                    ))
                    return

        random_index = randint(0, len(res) - 1)
        random_id = res[random_index]['messageID']

        random_message = db.get_content_message_id(self.bot.init_db, int(random_id))
        message = random_message['message']
        user_id = random_message['UserID']
        channel_id = random_message['channel']
        time = random_message['time']
        guild_id = ctx.message.guild.id

        link_message = "https://discord.com/channels/{}/{}/{}".format(guild_id, channel_id, random_id)

        embed = discord.Embed(
            title="🤖 Biboop, I love stats ! Here's my research...",
            color=utils.COLOR
        )
        embed.add_field(
            name="📚 Out of context :",
            value="In <#{}>'s channel, <@{}> sent: ".format(channel_id, user_id),
            inline=False
        )
        embed.add_field(
            name="📕 message :",
            value=message,
            inline=False
        )
        embed.add_field(
            name="📖 Context :",
            value=link_message,
            inline=False
        )
        embed.set_footer(
            text="Date : {}".format(time)
        )
        await ctx.send(embed=embed)
        if "https://" in message:
            await ctx.send(message)


def setup(bot):
    bot.add_cog(SettingsCommands(bot))
