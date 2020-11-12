import os

import discord
import pymysql.cursors

from dotenv import load_dotenv
import logging

logger = logging.getLogger('LSDStats')


def insertMessageInTable(message, connection):
    connection.ping(reconnect=True)
    user = message.author
    user_id = user.id
    content = message.content
    channel_id = message.channel.id
    time = message.created_at
    message_id = message.id

    try:
        sql = "INSERT INTO `messages` (`UserID`, `message`,`Channel`, `messageID`, `time`) VALUES (%s, %s, %s, %s, %s)"
        connection.cursor().execute(sql, (user_id, content, channel_id, message_id, time))
        logger.info("Collectings data from {} ".format(user))
        connection.commit()

    except Exception as e:
        logger.exception(e)



def update_accepting_users(user_id, connection, adding=True):
    try:
        if adding:
            sql = "INSERT INTO `accepts` (`UserID`) VALUES (%s)"
            logger.info("Adding UserID {}".format(userID))
        else:
            sql = "DELETE FROM `accepts` WHERE UserID='%s'"

        connection.cursor().execute(sql, user_id)
        logger.info("Updating UserID in accepts db {}".format(user_id))
        connection.commit()

    except Exception as e:
        logger.exception(e)



def get_user_id_accepts(connection, user_id):
    try:
        sql = "SELECT UserID FROM `accepts` WHERE UserID='%s'"
        logger.info("Select {} from accepts".format(user_id))

        with connection.cursor() as cur:
            cur.execute(sql, user_id)
            res = cur.fetchone()
            return res  # return None if is missed.

    except Exception as e:
        logger.exception(e)



def delete_message(connection, message_id):
    try:
        sql = "DELETE FROM `messages` WHERE messageID='%s'"

        connection.cursor().execute(sql, message_id)
        logger.info("Deleting {} from messages".format(message_id))
        connection.commit()

    except Exception as e:
        logger.exception(e)
