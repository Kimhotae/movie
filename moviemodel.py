import pymysql
from flask import Flask
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


mysqlSecret = config["SECRET"]["MYSQL_SECRET"]

MYSQL_HOST = 'localhost'
MYSQL_CONN = pymysql.connect(
    host=MYSQL_HOST,
    port=3306,
    user='hotae',
    passwd=mysqlSecret,
    db='movie',
    charset='UTF8'
)


def conn_mysqldb():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN
