import os
import discord

from discord.ext import commands
import logging

logger = logging.getLogger('LSDStats')


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


def get_nb_occ_msg(user=None, msg):
    pass