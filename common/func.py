import pymysql
import requests
import json
import conf.config as con

def get_TrackNo():
    """初始化数据库"""
    c=con.get_conf()

    db_host = c["host"]
    db_user = c["user"]
    db_password = c["password"]
    db_test_buyer = c["db_test_buyer"]
    db_test_user = c["db_test_user"]

    """连接数据库"""
    conn_buyer=pymysql.connct(host=db_host, user=db_user, password=db_password, database=db_test_buyer)
    cur_buyer=conn_buyer.cursor()
    sql_buyer='SELECT TrackNO FROM TrackInfo02 WHERE (Email = "123@qq.com")'
    cur_buyer.execute(sql_buyer)
    trackno_result=cur_buyer.fetchall()


