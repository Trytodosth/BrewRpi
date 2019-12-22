#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  brewSQL.py
#
#  This script can create SQLite3 DB
import sqlite3
import sys
import os
import datetime
import time
from dateutil import tz

# Timezones conversion because SQL uses UTC
from_zone = tz.tzutc()
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

# Default database
DBfolder = 'Databases'
DBdefault = 'CurrentBatch.db'
conn = sqlite3.connect(os.path.join(DBfolder, DBdefault))
curs = conn.cursor()


def createDB(args):
    DBname = ''
    if len(args) <= 1:
        DBname = DBdefault
    else:
        if args[1].endswith('.db'):
            DBname = args[1]
    if DBname:
        con = sqlite3.connect(os.path.join(DBfolder, DBname))
        with con: 
            cur = con.cursor() 
            cur.execute("DROP TABLE IF EXISTS Sensor_Data")
            cur.execute("CREATE TABLE Sensor_Data(timestamp DATETIME, currTemp NUMERIC, targetTemp NUMERIC, relayState NUMERIC)")
            cur.execute("DROP TABLE IF EXISTS TargetTemp_Data")
            cur.execute("CREATE TABLE TargetTemp_Data(timestamp DATETIME, targetTemp NUMERIC)")
        print(DBname + ' database successfully reset')


def insertSensorData(currTemp, targetTemp, relayState):
    con = sqlite3.connect(os.path.join(DBfolder, DBdefault))
    with con:
        cur = con.cursor() 
        cur.execute("INSERT INTO Sensor_Data VALUES(datetime('now'), %s, %s, %i)" % (currTemp, targetTemp, 1 if relayState else 0))
    

def getLastData():
    con = sqlite3.connect(os.path.join(DBfolder, DBdefault))
    with con: 
        cur = con.cursor() 
        for row in cur.execute("SELECT * FROM Sensor_Data ORDER BY timestamp DESC LIMIT 1"):
            print("Last raw Data logged on database: %s" % str(row))
            return row


def getHistData(numSamples):
    con = sqlite3.connect(os.path.join(DBfolder, DBdefault))
    with con: 
        cur = con.cursor() 
        cur.execute("SELECT * FROM Sensor_Data ORDER BY timestamp DESC LIMIT " + str(numSamples))
        data = cur.fetchall()
        dates = []
        measures = []
        targets = []
        for row in reversed(data):
            dates.append(row[0])
            measures.append(row[1])
            targets.append(row[2])
        return [datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").replace(tzinfo=from_zone).astimezone(LOCAL_TIMEZONE) for dt in dates], measures, targets
   
def maxRowsTable():
	for row in curs.execute("select COUNT(temp) from  Sensor_Data"):
		maxNumberRows = row[0]
	return maxNumberRows
    
    
    
            
def getTargetTempSQL():
    con = sqlite3.connect(os.path.join(DBfolder, DBdefault))
    with con: 
        cur = con.cursor()
        for row in cur.execute("SELECT targetTemp FROM TargetTemp_Data ORDER BY timestamp DESC LIMIT 1"):
            print("Target temperature according to DB: %s°C" % row[0])
            return row[0]
            
def setTargetTempSQL(inTemp):
    con = sqlite3.connect(os.path.join(DBfolder, DBdefault))
    with con: 
        cur = con.cursor()
        cur.execute("INSERT INTO TargetTemp_Data VALUES(datetime('now'), %s)" % inTemp)
            
    
def fillDB():
    print('Filling DB randomly...')
    insertSensorData(25.2, 26, 1)
    time.sleep(1)
    insertSensorData(25.7, 26, 1)
    time.sleep(1)
    insertSensorData(26.3, 26, 0)
    setTargetTempSQL(26)
    print('... Done!')
    
    
def displayTable():
    for row in curs.execute("SELECT * FROM Sensor_Data"):
        print(row)




def brewSQL(args=['']):
    #createDB(args)
    #fillDB()
    #displayTable()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(brewSQL(sys.argv))
