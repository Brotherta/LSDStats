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


def update_accepting_users(userID, connection, adding=True):  
    try:
        if adding:
            sql = "INSERT INTO `accepts` (`UserID`) VALUES (%s)"
            logger.info("Adding UserID {}".format(userID))
        else:
            sql = "DELETE FROM `accepts` WHERE UserID='%s'"

        connection.cursor().execute(sql, (userID))
        logger.info("Updating UserID in accepts db {}".format(userID))
        connection.commit()
    
    except Exception as e:
        logger.exception(e)

def get_user_id_accepts(connection, userID):
    try:
        sql = "SELECT UserID FROM `accepts` WHERE UserID='%s'"
        logger.info("Select {} from accepts".format(userID))

        with connection.cursor() as cur:
            cur.execute(sql, (userID))
            res = cur.fetchone()
            return res                  # return None is missed.

    except Exception as e:
        logger.exception(e)
