# bot.py
import os

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import pymysql.cursors

import src.settings as s
import src.database as db
import src.acceptingCollect as ac
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HOST = os.getenv('MyHOST')
DB = os.getenv('DATABASE')
USER = os.getenv('MyUSER')
PWD = os.getenv('MyPWD')

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
        super().__init__(command_prefix="s!") #help_command=_default
        self._load_extensions()
        self.remove_command("help")
        self._init_db = None

    def _load_extensions(self):
        for file in os.listdir("cogs/"):
            try:
                if file.endswith(".py"):
                    self.load_extension(f'cogs.{file[:-3]}')
            except Exception as e:
                print(e)
                
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        try :
            self._init_db = pymysql.connect(host=HOST,
                                            user= USER,
                                            password=PWD,
                                            db=DB,
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
    
    async def on_message(self, message): # cogs
        #print(message.author.id)
        user = message.author

        if not message.content.startswith('s!') and  str(user.id) in ac.YesList:  
            db.insertMessageInTable(message, self._init_db)

        elif message.content.startswith('s!salut'):
            if user.id == 585123574487187476:
                await message.channel.send("Bonjour {} trou d'balle.".format(user))
            else:
                await message.channel.send("Bonjour <@{}>.".format(user.id))

    def run(self, token, *args, **kwargs):
        try:
            super().run(token, *args, **kwargs)
        except KeyboardInterrupt:
            exit(0)


if __name__ == "__main__":
    bot=LSDBot()
    bot.run(TOKEN, reconnect = True)





