# bot.py
import os
import discord
import logging
import pymysql.cursors

from discord.ext import commands
from dotenv import load_dotenv


import src.utils as utils
import src.database as db
import data.acceptingCollect as ac


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
    
    async def on_message(self, message):
        userID = message.author.id
        is_accepting = db.get_user_id_accepts(self._init_db, userID)
        if is_accepting != None:  
            db.insertMessageInTable(message, self._init_db)
        elif str(userID) in ac.YesList:
            db.insertMessageInTable(message, self._init_db)

        await self.process_commands(message)

    async def on_reaction_add(self, reaction, user):
        if reaction.message.id == int(utils.get_msg_react_id()) and reaction.emoji == '✅' :
            if user.id != self.user.id:
                db.update_accepting_users(user.id, self._init_db)
                
        elif reaction.message.id == int(utils.get_msg_react_id()) and reaction.emoji == '❌' :
            if user.id != self.user.id:
                db.update_accepting_users(user.id, self._init_db, False)




if __name__ == "__main__":
    bot=LSDBot()
    bot.run(TOKEN, reconnect = True)





