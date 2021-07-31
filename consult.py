import time
import requests
import json
import getpass
from datetime import datetime

import mysql.connector

VtuberOfInterest = {
    'xuehusang': 477792,
    'kitzuki': 591892279,
}

mysqlHost = '172.17.0.4'
mysqlUsername = 'root'
mysqlPassword = ''

def inputMysqlPassword():
    global mysqlPassword
    mysqlPassword = getpass.getpass(prompt='MySQL Password: ')

def getFansNumber(UserUid):
    data = requests.get('https://api.bilibili.com/x/web-interface/card?mid=%d' % (UserUid))
    information = json.loads(data.text)
    uname = information['data']['card']['name']
    uid = information['data']['card']['mid']
    fans = information['data']['follower']
    return uname, uid, fans

def writeToDatabase(label, uname, uid, fans):
    mydb = mysql.connector.connect(
        host=mysqlHost,
        user=mysqlUsername,
        password=mysqlPassword,
        database=label
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO fans_number (uname, uid, fans) VALUES (%s, %s, %d)"
    val = (uname, uid, fans)

    mycursor.execute(sql, val)
    mydb.commit()


def main():
    inputMysqlPassword()

    while True:
        for label, uid in VtuberOfInterest.items():
            uname, uid, fans = getFansNumber(uid)
            writeToDatabase(label, uname, uid, fans)
            print (str(datetime.now()), uname, uid, fans)
        time.sleep(60)

if __name__ == '__main__':
    main()