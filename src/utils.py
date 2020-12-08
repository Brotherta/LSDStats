import os
import discord

import src.database as db
from discord.ext import commands
import logging

logger = logging.getLogger('LSDStats')
COLOR = 0xba0b0b


def write_msg_react_id(message_id):
    try:
        file = open('data/messageReaction.txt', "w")
        file.truncate(0)
        file.write("{}".format(message_id))
        file.close()

    except Exception as e:
        logger.exception(e)


def get_msg_react_id():
    try:
        r_id = ''
        file = open('data/messageReaction.txt', "r")
        r_id = file.read()
        file.close()
        return r_id

    except Exception as e:
        logger.exception(e)


def channel_to_channel_id(channel):
    if channel[:2] == "<#" and channel[-1] == ">":
        channel = int(channel[2:len(channel) - 1])
        return channel
    else:
        return 0



def get_occ_msg(connection, msg, user, channel):
    return db.get_occ_msg_data(connection, msg, user, channel)

