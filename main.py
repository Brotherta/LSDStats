# bot.py
import os
import discord
import logging
import pymysql.cursors

from discord.ext import commands
from dotenv import load_dotenv

import src.utils as utils
import src.database as db


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HOST = os.getenv('MyHOST')
DB = os.getenv('DATABASE')
USER = os.getenv('MyUSER')
PWD = os.getenv('MyPWD')

list_user_accept = []

logger = logging.getLogger('LSDStats')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='LSDStats.log',
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)
)
logger.addHandler(handler)


class LSDBot(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(command_prefix="s!")  # help_command=_default
        self.remove_command("help")
        self._load_extensions()
        self.init_db = None
        self.is_accepting = []
        self.accept_channel_id = 0


    def _load_extensions(self):
        for file in os.listdir("cogs/"):
            try:
                if file.endswith(".py"):
                    self.load_extension(f'cogs.{file[:-3]}')
            except Exception as e:
                print(e)


    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        try:
            self.init_db = pymysql.connect(host=HOST,
                                            user=USER,
                                            password=PWD,
                                            db=DB,
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor)
            self.is_accepting = db.get_all_user_id_accepts(connection=self.init_db)
            self.accept_channel_id = int(utils.get_msg_react_id())
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="🤖 s!help"))
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))


    async def on_message(self, message):
        user_id = message.author.id
        if str(user_id) in self.is_accepting:
            db.insert_message_in_table(message, self.init_db)
            await self.process_commands(message)
        elif message.author.id is self.user.id:
            await message.add_reaction('🤖')


    async def on_message_delete(self, message):
        user_id = message.author.id
        if str(user_id) in self.is_accepting:
            db.delete_message(self.init_db, message.id)


    async def on_message_edit(self, before, after):
        user_id = before.author.id
        if str(user_id) in self.is_accepting:
            db.delete_message(self.init_db, after.id)
            db.insert_message_in_table(after, self.init_db)


    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.accept_channel_id and str(payload.emoji) == '✅':
            if payload.user_id != self.user.id:
                db.update_accepting_users(payload.user_id, self.init_db)
                self.is_accepting = db.get_all_user_id_accepts(self.init_db)

        elif payload.message_id == self.accept_channel_id and str(payload.emoji) == '❌':
            if payload.user_id != self.user.id:
                db.update_accepting_users(payload.user_id, self.init_db, False)
                self.is_accepting = db.get_all_user_id_accepts(self.init_db)


    async def on_command_error(self, ctx, error):
        embed = discord.Embed(
            title="🤖 ❌ Biboop, I love stats ! But you're wrong !",
            color=utils.COLOR
        )
        embed.add_field(
            name="{} ...".format(error),
            value="📚 Try:  `s!help`\n\n",
            inline=False
        )
        await ctx.send(embed=embed)


if __name__ == "__main__":
    bot = LSDBot()
    bot.run(TOKEN, reconnect=True)
