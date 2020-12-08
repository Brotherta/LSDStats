import logging

logger = logging.getLogger('LSDStats')


def insert_message_in_table(message, connection):
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
            sql = "INSERT INTO `accepts`  (`UserID`) VALUES (%s)"
            logger.info("Adding UserID {}".format(user_id))
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


def get_all_user_id_accepts(connection):
    try:
        sql = "SELECT UserID FROM `accepts`"
        logger.info("Select all UserID from accepts")

        with connection.cursor() as cur:
            cur.execute(sql)
            res = cur.fetchall()
            res_list = [user["UserID"] for user in res]
            return res_list    # return a list of dictionary which contains user ids as value
    except Exception as e:
        logger.exception(e)


def get_occ_msg_data(connection, msg, user, channel):

    options = [msg, user, channel]
    tab_sql = [" message LIKE '%{}%'", " UserID={}", " Channel={}"]
    tab_info = [" wich contains '{}'", " written by {}", " on the channel {}"]

    try:
        sql = "SELECT COUNT(message) FROM `messages`"
        info = "Count occurencies of messages"
        nb_option = 0

        for i in range(3):
            if options[i] is not None:
                if nb_option == 0:
                    sql += " WHERE"
                else:
                    sql += " AND"

                sql += tab_sql[i].format(options[i])
                info += tab_info[i].format(options[i])
                nb_option += 1

        logger.info(info)

        with connection.cursor() as cur:
            cur.execute(sql)
            res = cur.fetchone()
            return res
    except Exception as e:
        logger.exception(e)


def get_talker_channel(connection, channel_id):
    try:
        sql = "SELECT UserID, COUNT(*) AS nb FROM messages WHERE Channel={} GROUP BY UserID ORDER BY nb DESC LIMIT 0,1;".format(channel_id)
        logger.info(sql)
        with connection.cursor() as cur:
            cur.execute(sql)
            res = cur.fetchone()
            return res  # return None if is missed.
    except Exception as e:
        logger.exception(e)


def get_all_msg_channel(connection, channel_id):
    try:
        sql = "SELECT COUNT(*) AS nb FROM messages WHERE Channel={};".format(channel_id)
        logger.info(sql)
        with connection.cursor() as cur:
            cur.execute(sql)
            res = cur.fetchone()
            return res  # return None if is missed.
    except Exception as e:
        logger.exception(e)


def get_all_message_id(connection, channel_id, limit):
    if channel_id != 0:
        channel_id_sql = "AND Channel like '%{}%'".format(channel_id)
    else:
        channel_id_sql = ""
    try:
        sql = "SELECT messageID FROM messages WHERE LENGTH(message)>{} {};".format(limit, channel_id_sql)
        logger.info(sql)
        with connection.cursor() as cur:
            cur.execute(sql)
            res = cur.fetchall()
            return res
    except Exception as e:
        logger.exception(e)


def get_content_message_id(connection, message_id):
    try:
        sql = "SELECT UserID, message, channel, time FROM messages WHERE messageID={}".format(message_id)
        logger.info(sql)
        with connection.cursor() as cur:
            cur.execute(sql)
            res = cur.fetchone()
            return res
    except Exception as e:
        logger.exception(e)
