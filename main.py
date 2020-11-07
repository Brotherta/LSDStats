# bot.py
import os

import os

import discord
import pymysql.cursors
from dotenv import load_dotenv

import src.settings as s
import src.database as db
import src.acceptingCollect as ac

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    #print(message.author.id)
    user = message.author

    if not message.content.startswith('s!') and  str(user.id) in ac.YesList:  
        await db.insertAuthorInTable(message)

    elif message.content.startswith('s!salut'):
        if user.id == 585123574487187476:
            await message.channel.send("Bonjour {} trou d'balle.".format(user))
        else:
            await message.channel.send("Bonjour <@{}>.".format(user.id))


# utf 8

client.run(TOKEN)