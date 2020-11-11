import os

import discord
import pymysql.cursors

from dotenv import load_dotenv
import logging

logger = logging.getLogger('LSDStats')



def insertMessageInTable(message, connection):
    connection.ping(reconnect=True)
    user = message.author
    userID = user.id
    content = message.content
    channelID = message.channel.id
    time = message.created_at


    try:
        sql = "INSERT INTO `messages` (`UserID`, `message`,`Channel`, `time`) VALUES (%s, %s, %s, %s)"
        connection.cursor().execute(sql, (userID, content, channelID, time))
        logger.info("Collectings data from {} ".format(user))
        connection.commit()

    except Exception as e:
        logger.exception(e)
