import os

import discord
import pymysql.cursors

from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('MyHOST')
DB = os.getenv('DATABASE')
USER = os.getenv('MyUSER')
PWD = os.getenv('MyPWD')

def insertAuthorInTable(message):
    user = message.author
    userID = user.id
    content = message.content
    channelID = message.channel.id
    time = message.created_at

    try:
        try :
            connection = pymysql.connect(host=HOST,
                                        user= USER,
                                        password=PWD,
                                        db=DB,
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
        
        sql = "INSERT INTO `messages` (`UserID`, `message`,`Channel`, `time`) VALUES (%s, %s, %s, %s)"
        try:
            connection.cursor().execute(sql, (userID, content, channelID, time))
            connection.commit()
        except Exception as e:
            print(e)
        
        connection.close()
    except:
        print("Connection db failed.")