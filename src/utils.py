import os
import discord

from discord.ext import commands
import logging

logger = logging.getLogger('LSDStats')

def write_msg_react_id(messageID):
    try:
        file = open('data/messageReaction.txt', "w")
        file.truncate(0)
        file.write("{}".format(messageID))
        file.close()

    except Exception as e:
        logger.exception(e)
    
def get_msg_react_id():
    try:
        Rid =''
        file = open('data/messageReaction.txt', "r")
        Rid = file.read()
        file.close()
        return Rid

    except Exception as e:
        logger.exception(e)
    