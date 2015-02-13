# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 11:12:51 2014

@author: koxmoz

This program is GPL v3, read the LICENSE file.
"""

import datetime
from time import sleep
from gpx import Gpx_Data, read_gpx_files
from db import db_lite

# import readline
DB = db_lite()


class Runner(object):
    """
    runner profile
    """
    def __init__(self, ID, name, age, weight, sex, preference):
        self.ID = ID
        self.name = name
        self.age = age
        self.weight = weight
        self.sex = sex
        self.pref = preference
        self.total_distance = None
        self.total_time = None
        self.total_runs = None
        self.faster_run = None


class Activity(object):
    """
    it's an instance of the activity in the database, id_a it's de 'ID of the
    activit' while runner it's the runner ID in the database
    """
    def __init__(self, id_a, date, typerun, distance, time, runner):
        self.id_a = id_a
        self.date = date
        self.typerun = typerun
        self.distance = distance
        self.time = time
        self.runner = runner  # ID runner
        self.pace = None
        self.average_speed = None

    def pace_and_speed(self):
        """
        sets pace and average speed for manual entry, for gpx entry use the
        moduel
        """
        time = [float(x) for x in self.time.split(":")]
        time = datetime.timedelta(hours=time[0], minutes=time[1],
                                  seconds=time[2])
        self.pace = round((time.total_seconds() / 60) / float(self.distance),
                          2)  # round 2 decimals
        self.average_speed = round(float(self.distance) / (time.total_seconds() / 3600), 2)


def load_runners():
    """
    load an instance of runner class for each profile in the database
    """
    DB.read_profiles()
    profiles = []

    for runner in DB.runners:
        runner_id, name, age, weight, sex, pref = runner
        profiles.append(Runner(runner_id, name, age, weight, sex, pref))

    return profiles


def new_runner():
    """
    This function create a new runner
    """
    name = raw_input("Please write your name: ")
    age = raw_input("Write your age: ")
    weight = raw_input("Write your weigth: ")
    sex = raw_input("Write your sex (male or female): ")
    preference = 2
    while preference > 1:
        preference = int(raw_input("Write 0 (zero) for 'mi and lb' or"
                                   + " 1 (one) for 'km and kg': "))
    print "\n"

    DB.insert_new_runner([name, age, weight, sex, str(preference)])
    return


def select_runner(profiles):
    """
    Show the Runners (instanced) and the option to add a new runner, the user
    choice by a number...
    """
    print "{0:^3} : {1:^3}".format("0", "Create a New Runner")
    # Printing the option
    for runner in profiles:
        print "{0:^3} : {1:^3}".format(runner.ID, runner.name)

    # selection of the number
    while True:
        print "Write the Number of the runner"
        try:
            runner = int(raw_input("Number: "))
            if runner <= len(profiles) and runner >= 0:
                break
        except ValueError:
            print "just Numbers...\n"
    # option new Runner
    if runner == 0:
        new_runner()
        return select_runner(load_runners())
    # else selected runner
    return profiles[runner - 1]


def set_extra_info(profile):
    """
    Set the extras attributes to the instance of the selected runner
    """
    DB.read_activities(profile.ID)
    runs = DB.activities[:]
    # set total runs
    profile.total_runs = len(runs)

    if profile.total_runs > 0:
        # setting up total distance
        total_distance = []
        for run in runs:
            total_distance.append(float(run[3]))

        profile.total_distance = sum(total_distance)

        # setting up the total time
        # set total_time in 0
        total_time = datetime.timedelta()
        for run in runs:
            # split the string into a list
            time = run[4].split(":")
            # convert to a float number each element
            time = [float(t) for t in time]
            # add to total time the time of the run
            total_time = total_time + datetime.timedelta(hours=time[0],
                                                       minutes=time[1],
                                                       seconds=time[2])
        # the __str__() is becouse time is in seconds, and in this way
        # return hh:mm:ss.ms
        profile.total_time = total_time.__str__()

        # set fasted run
        speed = 0
        for run in runs:
            if float(run[6]) > speed:
                profile.faster_run = run[1]
                speed = run[6]
    else:
        profile.total_distance = 0
        profile.total_time = datetime.timedelta().__str__()
        profile.total_runs = 0
        profile.faster_run = 0
    return


def show_data(runner):
    """
    print the screen presentation
    """

    print '{0:<16} {1:^16} {2:>16}'.format("#" * 12, "Welcome..!", "#" * 12)
    print '{0:<16} {1:^16} {2:>16}'.format("#" * 12,
                                           runner.name, "#" * 12)
    print ""
    print '{0:<16} {1:^16} {2:>16}'.format(" "*10, "#"*10, " "*10)
    print ""
    print '{0:<16} {1:^16} {2:>16}'.format(
        ("Age: " + str(runner.age)),
        ("Weight: " + str(runner.weight)),
        ("Sex: " + runner.sex))
    print '{0:<16} {1:^16} {2:>16}'.format(
        ("Total Distance :" + str(runner.total_distance)),
        ("Total Time: " + str(runner.total_time)),
        ("Total Runs: " + str(runner.total_runs)))
    print '{0:<16} {1:^16} {2:>16}'.format(" "*10,
                                        "Fasted Run: " + str(runner.faster_run),
                                           " "*10)
    print ""
    return


def load_activity(runner):
    """
    return a list of istanced activity
    """
    DB.read_activities(runner.ID)
    activities = []

    # making an instance of each activity
    for activity in DB.activities:
        activities.append(Activity(activity[0],
                                   activity[1],
                                   activity[2],
                                   activity[3],
                                   activity[4],
                                   activity[7]))
    # return the list
    return activities


def list_activities(activities, header=True):
    """
    Print out the list of activities. If header is false, dont print it out.
    """

    if header:
        print ""
        print '{0:^10}|{1:^10}|{2:^10}|{3:^10}|{4:^10}|{5:^10}|{6:^10}'.format(
            "Number",
            "Date",
            "Type Run",
            "Distance",
            "Time",
            "Pace",
            "Avg. Speed")
    if len(activities) > 0:
        for activity in activities:
            activity.setP_and_AS()
            print '{0:^10}|{1:^10}|{2:^10}|{3:^10}|{4:^10}|{5:^10}|{6:^10}'.format(
                activities.index(activity),
                activity.date,
                activity.typerun,
                activity.distance,
                activity.time,
                activity.pace,
                activity.average_speed)
            print "{0:^3} : {1:^3}".format("c", "Back to main menu")
    else:
        print "No activities yet..."
    return


def time_input():
    """
    return a string like this "hh:mm:ss"
    """
    # get the time info
    while True:
        time = [raw_input("Introduce the hours: "),
                raw_input("introduce the minutes: "),
                raw_input("introduce the secods: ")
                ]
        # in case a null imput
        for item in time:
            if item == "":
                time[time.index(item)] = 0
        # Check Number value, and if there is letters
        try:
            if float(time[0]) >= 24 \
                    and float(time[1]) >= 60 \
                    and float(time[2]) >= 60:
                print "Hours should be less than 24, Minutes \
                                       and secods less than 60"
                pass
        # If there is an exception just print and pass (supoustly)
        except ValueError:
            print "Just Numbers..."
        break
    # format in hh:mm:ss
    time = ":".join(time)
    return time


def new_gpx_activity(runner, activities):
    """
    create an activity from a GPX file
    """
    gpxfiles = read_gpx_files()
    if len(gpxfiles) == 0:
        print "You must copy your gpx files in the folder 'gpxfiles/'"
        return activities

    print "GPX Files"
    print ""
    for gfile in gpxfiles:
        # cut of the "gpxfiles/" to get the simple file name
        print "{0:^3} : {1:^3}".format(gpxfiles.index(gfile),
                                       gfile.replace("gpxfiles/", ""))
    while True:
        try:
            select_option = int(raw_input("Introduce the number of the file: ")
                                )
            if select_option > len(gpxfiles):
                print "The Number sould be less than " + str(select_option)
                pass
        except ValueError:
            print "Just Numbers..."
            pass
        break

    gpxactivity = Gpx_Data(gpxfiles[select_option])
    gpxactivity.gpx_parse()
    gpxactivity.total_distance()
    gpxactivity.time_date()
    gpxactivity.pace_and_speed(runner.pref)
    pref = int(runner.pref)  # 0 for miles and 1 for kilometers
    # save the new activity in the database
    DB.insert_new_activity([gpxactivity.gettotal_info("date"),
                           "R",
                            gpxactivity.gettotal_info("tdistance")[pref],
                            gpxactivity.gettotal_info("ttime"),
                            gpxactivity.gettotal_info("pace"),
                            gpxactivity.gettotal_info("speed"),
                            runner.ID])
    DB.read_activities(runner.ID)
    # variables for the new (and last) instace from the database
    id_a, date, typerun, distance, time, pace, speed, runner_id = DB.activities[-1]
    activity_new = Activity(id_a, date, typerun, distance, time, runner_id)
    activity_new.pace_and_speed()

    activities.append(activity_new)
    return activities


def new_activity(runner, activities):
    """
    Creates a new activity, append to the end of the file, instances and append
    to the list activities.
    Return activities list updated
    """
    id_a = len(activities)
    date = raw_input("Introduce the date (dd/mm/yy): ")
    typerun = raw_input("Introduce the activity type 'R' for a race or 'T' \
                        for a trining session: ")
    distance = raw_input("Introduce the distance: ")
    time = time_input()  # function to input time
    # new instance
    activity_new = Activity(id_a, date, typerun, distance, time, runner.ID)

    print "{:^}".format("=" * 20)
    list_activities([activity_new])

    # ask for confirmation, write the file if it's yes, if it's no makes a
    # recursive call, otherwise ask again.
    while True:
        is_okk = raw_input("Is this information is ok? (yes or no): ")
        if is_okk == "yes":
            activity_new.pace_and_speed()
            DB.insert_new_activity([activity_new.date,
                                    activity_new.typerun,
                                    activity_new.distance,
                                    activity_new.time,
                                    activity_new.pace,
                                    activity_new.average_speed,
                                    activity_new.runner
                                    ])
            break  # close the loop
        elif is_okk == "no":
            return new_activity(runner, activities)
        else:
            print "Just 'yes' or 'no'."
    activities.append(new_activity)
    return activities


def mod_activity(runner, activities):
    """
    get an activity and mod the a data in the instance and DataBase

    retruns an activites list moded
    """
    list_activities(activities)
    data_mod = ["Date", "Type", "Distance", "Time"]
    # loop to ask again if introduces a bad answer
    while True:
        selec_activity = raw_input("Introduce the number of the activity: ")
        if selec_activity in ["C", "c"]:
            return activities
        else:
            try:
                selec_activity = int(selec_activity)
            # In case introduce a wron string
            except ValueError:
                print "Just Numbers from '0' to " + str(len(activities))

            if selec_activity > len(activities):
                pass
            else:
                actual_data = [activities[selec_activity].date,
                               activities[selec_activity].typerun,
                               activities[selec_activity].distance,
                               activities[selec_activity].time]

                # Print a list of type data and data
                for adata in actual_data:
                    index = actual_data.index(adata)
                    print "{0:^5} {1:^5} {2:^5}".format(index, data_mod[index],
                                                        adata)
                # loop to ask again if introduces a bad answer
                while True:
                    selec_data = raw_input("Introduce the number of the \
                                            data: ")
                    if selec_data is "0":
                        new_data = raw_input("Introduce the new Date: ")
                        activities[selec_activity].date = new_data
                        break
                    elif selec_data is "1":
                        new_data = raw_input("Introduce the new Type Run: ")
                        activities[selec_activity].typerun = new_data
                        break
                    elif selec_data is "2":
                        new_data = raw_input("Introduce the new Distance: ")
                        activities[selec_activity].distance = new_data
                        activities[selec_activity].setP_and_AS()
                        break
                    elif selec_data is "3":
                        time = time_input()
                        activities[selec_activity].time = time
                        activities[selec_activity].setP_and_AS()
                        break
            # the next two 'else' it is in case introduce an out of range index
                    else:
                        print "Just Numbers from '0' to '3'..."
        break
    # upgrade the database
    DB.upgrade_activity([activities[selec_activity].id_a,
                         activities[selec_activity].date,
                         activities[selec_activity].typerun,
                         activities[selec_activity].distance,
                         activities[selec_activity].time,
                         activities[selec_activity].pace,
                         activities[selec_activity].average_speed,
                         activities[selec_activity].runner])
    # return the activites list
    return activities


def del_activity(runner, activities):
    """
    select the activity to delete
    """
    list_activities(activities)
    while True:
        select_activity = raw_input("Introduce the number of the activity: ")
        if select_activity in ["C", "c"]:
            return activities
        else:
            try:
                select_activity = int(select_activity)
            except ValueError:  # In case get a string
                print "Just Numbers from '0' to " + str(len(activities))
            if select_activity > len(activities):
                print "Just Numbers from '0' to " + str(len(activities))
                pass
        break
    DB.delete_activity(activities[select_activity].id_a, runner.ID)
    activities.remove(activities[select_activity])
    return activities


def mod_runner(runner):
    """
    modified the runner instance selected and the database
    """
    data = [runner.name,
            runner.age,
            runner.weight,
            runner.sex,
            runner.pref]

    for item in data:
        print "{0:^3} : {1:^3}".format(data.index(item), item)
    print "{0:^3} : {1:^3}".format("c", "Back to main menu")
    while True:
        selec_data = raw_input("Introduce the Number: ")

        if selec_data is "0":
            new_data = raw_input("Introduce the new Name: ")
            runner.name = new_data
            break
        elif selec_data is "1":
            new_data = raw_input("Introduce the new Age: ")
            runner.age = new_data
            break
        elif selec_data is "2":
            new_data = raw_input("Introduce the new Weight: ")
            runner.weight = new_data
            break
        elif selec_data is "3":
            new_data = raw_input("Introduce the new Sex: ")
            runner.sex = new_data
            break
        elif selec_data is "4":
            while True:
                new_data = raw_input("Introduce the new Preference \
                                     '0' or '1': ")
                if new_data not in ["1", "0"]:
                    print "Just '0' or '1'"
                    pass
                break
            runner.pref = new_data
            break
        elif selec_data in ["c", "C"]:
            return
        else:
            print "Just Number from '0' to '4'...\n"

    # upgrade database
    DB.upgrade_profile([runner.ID, runner.name, runner.age,
                        runner.weight, runner.sex, runner.pref])
    return


def main_action():
    """
    Start the program, give th welcome and show the options to select or
    create a new runner.
    And the action that can do, add, mod or delet activities. at the en exit.
    """
    print """
Welcome to...
                 KORRER

An app to keep the tracks of your times in running...

    """
    sleep(1)
    print "Loading the runners profiles...\n"
    sleep(1)
    runners = load_runners()
    if len(runners) is 0:
        print "Is this your first time?"
        new_runner()
        runners = load_runners()

    sleep(1)
    print "LogIn...\n"
    runner = select_runner(runners)
    set_extra_info(runner)
    show_data(runner)
    activities_list = load_activity(runner)

    options = ["View Activities", "Add New Activity", "Modefy an Activity",
               "Delete an Activity", "Configuration", "Exit"]

    # something like a main loop??
    while True:
        sleep(1)
        print ""
        print "=" * 15
        print "{0:^3} : {1:^3}".format("Number Option", "Option")
        for item in options:
            print "{0:^3} : {1:^3}".format(options.index(item), item)

        selec_option = raw_input("Whats you wants to do? (option Number): ")
        print "=" * 15
        print ""
        if selec_option is "0":
            list_activities(activities_list)
        elif selec_option is "1":
            while True:
                print "{0:^3} : {1:^3}".format("0", "Manual Entry")
                print "{0:^3} : {1:^3}".format("1", "GPX File")
                print "{0:^3} : {1:^3}".format("c", "Back to main menu")
                selec_option = raw_input("(option Number): ")
                if selec_option is "0":
                    activities_list = new_activity(runner, activities_list)
                    break
                elif selec_option is "1":
                    activities_list = new_gpx_activity(runner, activities_list)
                    break
                elif selec_option in ["c", "C"]:
                    break
                else:
                    print "wron option"
        elif selec_option is "2":
            activities_list = mod_activity(runner, activities_list)
        elif selec_option is "3":
            activities_list = del_activity(runner, activities_list)
        elif selec_option is "4":
            mod_runner(runner)
        elif selec_option is "5":
            print " Are you gonna run..?\n Have a nice Run!!!"
            break
        else:
            print "Nop, Just numbers from '0' to '5'...\n"
    return

if __name__ == '__main__':
    try:
        main_action()
    except (KeyboardInterrupt, SystemExit):
        pass
