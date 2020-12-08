from discord.ext import commands
import discord
import src.utils as utils


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(
            title="🤖 Biboop, I love stats ! Need Help ?",
            color=utils.COLOR
        )
        embed.add_field(
            name="Count commands !",
            value="📚 `s!count [-u @someone] [-m \"message\"] [-c #channel]`\nIsn't hard to understand right ?",
            inline=False
        )
        embed.add_field(
            name="Quote commands !",
            value="📚 `s!quote [#channel]`\nGive a sentence or a word out of his context\n\n\n\n",
            inline=False
        )
        embed.add_field(
            name="Talker commands !",
            value="📚 `s!talker [#channel]`\n"
                  "Give the user who's the most active of the server, or in a specific channel.",
            inline=False
        )
        embed.add_field(
            name="Salut commands !",
            value="📚 `s!salut`\nI'm really nice !",
            inline=False
        )
        embed.set_footer(
            text="Work in progress... give me idea to improve myself !",
            icon_url=ctx.me.avatar_url
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))

