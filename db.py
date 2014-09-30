# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 22:34:15 2014

@author: koxmoz

this module provide to the main app (runner.py) the ability to comunicate with
the DB (data.db), this module shoud check if the db files exist, create one
if dosent exist, and apply the schema for the db.

Insert new data in RUNNER and ACTIVITY tables. Update data for bouth, and 
delete.

Create a list of Runners and Activities,
"""

import sqlite3
from os import listdir

class dblite(object):
    def __init__(self):
        self.dbfile = "data.db"
        self.dbcheck = self.checking()
        self.runners = []
        self.activities = []

    def checking(self):
        if self.dbfile in listdir("."):
            return True
        else:
            conn = sqlite3.Connection("data.db")
            cur = conn.cursor()
            cur.execute("""CREATE TABLE RUNNER (
					ID		INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					name 	TEXT(50),
					age 	     INTEGER(2),
					weight 	INTEGER(3),
					sex		TEXT(20),
					pref	     INTEGER(1)
                         )
					""")
            cur.execute(""" CREATE TABLE ACTIVITY (
					ID_A	    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					date	    DATETIME,
					type	    TEXT(1),
					distance INTEGER,
					time	    DATETIME,
					ID	    INTEGER NOT NULL,
                         FOREIGN KEY(ID) REFERENCES RUNNER(ID)
                         )
                         """)
            conn.commit()
            cur.close()
            conn.close()
        return True

    def insert_new_runner(self, data_list):
        name, age, weight, sex, pref = data_list
        
        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO RUNNER VALUES\
                    (null, '%s', '%s', '%s', '%s', '%s')" %\
                          (name, age, weight, sex, pref))
        conn.commit()
        cur.close()
        conn.close()
        return
    
    def read_profiles(self):
        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        table_runner = cur.execute("SELECT * FROM RUNNER")
        
        for runner in table_runner.fetchall():
            if runner not in self.runners:
                self.runners.append(runner)
        conn.commit()
        cur.close()
        conn.close()
        return

    def update_profile(self, data_list):
        ID, name, age, weight, sex, pref = data_list
        
        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        cur.execute("UPDATE RUNNER SET name='%s', \
                                       age='%s', \
                                       weight='%s' \
                                       sex='%s', \
                                       pref='%s' \
                                       WHERE ID= %S" %\
                                       (name, age, weight, sex, pref, ID))
        conn.commit()
        cur.close()
        conn.close()
        
        self.runners = []
        self.read_profiles()
        return
    
    def insert_new_activity(self, data_list):
        date, typerun, distance, time, runner_ID = data_list

        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO ACTIVITY VALUES\
                    (null, '%s', '%s', '%s', '%s', '%s')" %\
                         (date, typerun, distance, time, runner_ID))
        conn.commit()
        cur.close()
        conn.close()
        return

    def read_activities(self, runner_ID):
        """
        return the activities, of the runner selected
        """
        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        table_activities = cur.execute("SELECT * FROM ACTIVITY WHERE ID='%s'" %\
                                                                    (runner_ID))
        
        for activity in table_activities.fetchall():
            if activity not in self.activities:
                self.activities.append(activity)
        conn.commit()
        cur.close()
        conn.close()
        return

    def upgrade_activity(self, data_list):
        ID_A, date, typerun, distance, time, runner = data_list
        
        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        cur.execute("UPDATE RUNNER SET date='%s', \
                                       typerun='%s', \
                                       distance='%s' \
                                       time='%s', \
                                       WHERE ID_A= %S" %\
                                       (date, typerun, distance, time, ID_A))
        conn.commit()
        cur.close()
        conn.close()
    
        self.activities = []    
        self.read_activities()
        pass
    
    
print "testing"
print "·" * 10
print "testing runner"
db = dblite()
db.insert_new_runner(["kox", "25", "78", "male", "1"])
db.insert_new_runner(["moz", "19", "90", "male", "1"])
db.read_profiles()

print db.runners
print "·" * 10
for x in db.runners:
    print x

print "·" * 10
print "testing activities"
db.insert_new_activity(["03-12-14", "R", "10", "00:40:00", "1"])
db.insert_new_activity(["03-12-14", "R", "5", "00:20:00", "1"])
db.read_activities("1")

for x in db.activities:
    print x
    
print "end"


