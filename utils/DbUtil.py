# coding=utf-8
import sys, os, time
import logging, random, uuid
import datetime
from datetime import datetime, timedelta
from random import choice
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

#from log_linux import Logger

#elogger = Logger('../logs/DbErr.log', clevel=logging.WARN, Flevel=logging.WARN)

# 以下值要根据实际情况修改
sys_ip = '127.0.0.1'

class DbOper:
    """docstring for ClassName"""
    def __init__(self, arg):
        self.arg = arg

    def insertIosAppDB(self, app_information):
        conn = MySQLdb.connect(sys_ip, "root", "62283748", "tase", 3306, charset="utf8")
        cursor = conn.cursor()
        try:
            nums = [8,10,11,12,13,14]
            sql = """INSERT IGNORE INTO `ios_app_info` (`WRAPPERID`, `WRAPPERNAME`, `APPID`, `URL`, `SIZE`, 
            `OSVERSION`, `UPDATETIME`, `TITLE`, `VERSION`, `DOWNLOADID`, `SUBJECT`, 
            `OS`, `DESCRIPTION`, `COUNTRY`, `IMAGEURL`, `PRICE`, `DEVICE`, 
            `DEVELOPER`, `APPPATH`, `SAVETIME`, `ISAPPLOADED`)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'iOS', 
             %s, %s, %s, %s, '', %s, NULL, %s, '0')"""
            
            timeStruct = time.strptime(app_information["updatedTime"], "%Y-%m-%dT%H:%M:%SZ")
            strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)
            Tjzsj = datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")
            tomorrow = Tjzsj + timedelta(hours=choice(nums),minutes=5)
            tomorrow = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
            print 'strTime:', strTime, 'choice(nums):', choice(nums), 'tomorrow:', tomorrow
            tmp = [(app_information["wrapperId"], app_information["wrapperName"], app_information["appIdstr"], app_information["url"], app_information["size"], app_information["osVersion"], strTime, app_information["appName"], app_information["appVersion"], app_information["downloadUrl"], app_information["category"], app_information["description"], app_information["country"], ";".join(app_information["snapshotUrlList"]), app_information["price"], app_information["developerName"], tomorrow)]
            cursor.executemany(sql, tmp)
        except Exception as msg:
            conn.rollback()
            print 'sql Error:', str(msg)
            #elogger.error('Error:' + str(msg))

        conn.commit()
        cursor.close()
        conn.close()
        print 'OK'

#main function
if __name__ == '__main__':
    dbOper = DbOper('TEST')
    dbOper.test_insertDB()