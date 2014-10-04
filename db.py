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


class db_lite(object):
    """
    Do the connection betwen the sqlite db and the runner.py program
    """
    def __init__(self):
        self.dbfile = "data.db"
        self.dbcheck = self.checking()
        self.runners = []
        self.activities = []

    def checking(self):
        """
        check if the database exists, and create a new one, or return True
        """
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
                        typerun	    TEXT(1),
                        distance INTEGER,
                        time	    DATETIME,
                        pace     INTEGER,
                        speed    INTEGER,
                        ID	    INTEGER NOT NULL,
                        FOREIGN KEY(ID) REFERENCES RUNNER(ID)
                        )
                        """)
            conn.commit()
            cur.close()
            conn.close()
        return True

    def insert_new_runner(self, data_list):
        """
        get a list (data_list) wiht the info of the runner and save into the
        database
        """
        name, age, weight, sex, pref = data_list

        conn = sqlite3.Connection(self.dbfile)
        cur = conn.cursor()
        cur.execute("INSERT INTO RUNNER VALUES\
                    (null, '%s', '%s', '%s', '%s', '%s')" %
                    (name, age, weight, sex, pref))
        conn.commit()
        cur.close()
        conn.close()
        return

    def read_profiles(self):
        """
        read the runnes in the database and add them to list of the class
        """
        conn = sqlite3.Connection(self.dbfile)
        cur = conn.cursor()
        table_runner = cur.execute("SELECT * FROM RUNNER")

        for runner in table_runner.fetchall():
            if runner not in self.runners:
                self.runners.append(runner)
        conn.commit()
        cur.close()
        conn.close()
        return

    def upgrade_profile(self, data_list):
        """
        upgrade the info of the profiles
        """
        id_r, name, age, weight, sex, pref = data_list

        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        cur.execute("UPDATE RUNNER SET name='%s', \
                                       age='%s', \
                                       weight='%s', \
                                       sex='%s', \
                                       pref='%s' \
                                       WHERE ID='%s'" %
                    (name, age, weight, sex, pref, id_r))
        conn.commit()
        cur.close()
        conn.close()

        self.runners = []
        self.read_profiles()
        return

    def delete_profile(self, id_r):
        """
        delete the selected profile (ID)
        """
        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM RUNNER WHERE ID= %s" % (id_r))
        conn.commit()
        cur.close()
        conn.close()

        self.runners = []
        self.read_profiles()
        return

    def insert_new_activity(self, data_list):
        """
        inser a new activity in the database, but dont add them to the list
        self.activities
        """
        date, typerun, distance, time, pace, speed, runner_id = data_list

        conn = sqlite3.Connection(self.dbfile)
        cur = conn.cursor()
        cur.execute("INSERT INTO ACTIVITY VALUES\
                    (null, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %
                    (date, typerun, distance, time, pace, speed, runner_id))
        conn.commit()
        cur.close()
        conn.close()
        return

    def read_activities(self, runner_id):
        """
        return the activities, of the runner selected
        """
        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        table_activities = cur.execute("SELECT * FROM ACTIVITY WHERE ID='%s'" %
                                       (runner_id))

        for activity in table_activities.fetchall():
            if activity not in self.activities:
                self.activities.append(activity)
        conn.commit()
        cur.close()
        conn.close()
        return

    def upgrade_activity(self, data_list):
        """
        upgrade the info of an activit and add them to the list of the class
        """
        id_a, date, typerun, distance, time, pace, speed, runner = data_list

        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        cur.execute("UPDATE ACTIVITY SET date='%s', \
                                       typerun='%s', \
                                       distance='%s', \
                                       time='%s', \
                                       pace='%s', \
                                       speed='%s' \
                                       WHERE ID_A='%s'" %
                    (date, typerun, distance, time, pace, speed, id_a))
        conn.commit()
        cur.close()
        conn.close()

        self.activities = []
        self.read_activities(runner)
        return

    def delete_activity(self, id_a, runner):
        """
        delete an activity and update the list of the class, self.activities
        """
        conn = sqlite3.Connection("data.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM ACTIVITY WHERE ID_A= %s" % (id_a))
        conn.commit()
        cur.close()
        conn.close()

        self.activities = []
        self.read_activities(runner)
        return
