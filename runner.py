# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 11:12:51 2014

@author: koxmoz
"""
import os
import datetime
import csv
import fileinput
from time import sleep
from gpx import *
# import readline
profiles_folder = "profiles/"

class Runner(object):
    """
    runner profile
    """
    #TODO erase all the parameters to add them by an asignation
    def __init__(self, name, age, weight, sex, preference):
        self.ID = None
        self.name = name
        self.age = age
        self.weight = weight
        self.sex = sex
        self.pref = preference
        self.totaldistance = None
        self.totaltime = None
        self.totalruns = None
        self.fastedrun = None


class Activity(object):
    def __init__(self, date, typerun, distance, time,  runner):
        self.ID = None
        self.date = date
        self.typerun = typerun
        self.distance = distance
        self.time = time
        self.runner = runner # ID runner
        self.pace = None
        self.average_speed = None
    
    def setP_and_AS(self):
        """
        sets pace and average speed
        """
        time = [float(x) for x in self.time.split(":")]
        time = datetime.timedelta(hours=time[0], minutes=time[1], \
                                  seconds=time[2])
        self.pace = round((time.total_seconds() / 60) / float(self.distance), 2)
        self.average_speed = round(float(self.distance) / (time.total_seconds() / 3600), 2)
        

def readProfiles():
    """ 
    Read the files in the profile folder and return a list of profile    
    """
    # I'm not shure how clear is this 
    profiles_files = [(profiles_folder + afiles) \
                    for afiles in os.listdir(profiles_folder)]
    return profiles_files

def newRunner():
    """
    This function creates the first runners or create a new runner
    
    """
    def ingressProfileData():
        """
        get data and return a list with it
        """
        name = raw_input("Please write your name: ")
        age = raw_input("Write your age: ")
        weight = raw_input("Write your weigth: ")
        sex = raw_input("Write your sex (male or female): ")
        preference = 2
        while preference > 1:
            preference = int(raw_input("Write 0 (zero) for 'mi and lb' or"\
                                           + " 1 (one) for 'km and kg': "))
        print "\n"
        return [name, age, weight, sex, str(preference)]

    #TODO coment this function, it's no needed any more
    def createFile(name):
        """
        Create a file with the given name
        """
        #if the files do not exist create a new one
        afile = open((profiles_folder + name + ".csv"), "a")
        data_list = ingressProfileData()
        afile.write(",".join(data_list) + "\n")
        afile.write("Date,Type,Distance,Time,Pace,Speed" + "\n")
        afile.close()
        return
    #TODO coment this seccion too, 
    profiles_files = readProfiles()
    name = ""
    if len(profiles_files) > 0:
        print "Creating a new Profile...\n"
        #get the numbers in the last file
        for char in profiles_files[-1]:
            if str.isdigit(char):
                name = name + char
        name = "r" + str(int(name) + 1)
        createFile(name)
    else:
        print "There is no runners Profiles, lets create the first Profile..."
        name = "r1"
        createFile(name)
    return 


def loadRunners(profiles_files):
    """
    load an instance of runner class for each profile file and the file dir
    """
    profiles = []
    for afile in profiles_files:
        file_name = afile
        afile = open(afile, "rb")
        # I just have to remove the \n at the end of the line
        profiles.append((afile.readlines()[0].replace("\n", "") + "," + \
                         file_name).split(","))
        afile.close()

    for profile in profiles:
        # in case the instace have some imformation we dosen't wont lose
        if isinstance(profile[0], Runner):
            profiles[profiles.index(profile)] = profile[0]
        else:
            profile[0] = Runner(profile[0], profile[1], profile[2], \
                                profile[3], \
                                profile[4])
            # Replace the complete list for the name. to know the what runner 
            # are instanced.
            profiles[profiles.index(profile)] = [profile[0], profile[-1]]
    
    return profiles

def selectRunner(profiles):
    """
    Show the Runners (instanced) and the option to add a new runner, the user
    choice by a number...
    """
    list_option = []
    for profile in profiles:
        list_option.append(profile)
    print "{0:^3} : {1:^3}".format("0", "Create a New Runner")
    # Printing the option
    for option in list_option:
        print "{0:^3} : {1:^3}".format(list_option.index(option) + 1, 
                                       option[0].name)
    # selection of the number
    while True:
        print "Write the Number of the runner"
        try:
            runner = int(raw_input("Number: "))
            break
        except ValueError:
            print "just Numbers...\n"
    # option new Runner
    if runner == 0:
        newRunner()
        return selectRunner(loadRunners(readProfiles()))
    # selected runner
    return profiles[runner - 1]


def setExtraInfo(profile):
    """
    Set the extras attributes to the instance of the selected runner
    """
    # making a dictionarie to work whit the info
    afile = open(profile[-1], "r")
    index = 0
    runs = {}
    for line in afile.readlines():
        if index < 2:
            # dont need the firsts 2 lines, its the basic info profile
            # and the column header
            index += 1
            continue
        runs[index -2] = line.replace("\n", "").replace("\r", "").split(",")
        index += 1
    afile.close()

    #set total runs
    profile[0].totalruns = len(runs)
    
    if profile[0].totalruns() > 0:
        ## setting up the extra info in the 
        totaldistance = []
        for run in runs.itervalues():
            totaldistance.append(float(run[2]))
            
        profile[0].totaldistance = sum(totaldistance)
    
        ## setting up the total time
        # set totaltime in 0
        totaltime = datetime.timedelta()
        for run in runs.itervalues():
            # split the string into a list
            time = run[3].split(":")
            # convert to a float number each element
            time = [float(t) for t in time]
            # add to total time the time of the run
            totaltime = totaltime + datetime.timedelta(hours=time[0], \
                                                       minutes=time[1], \
                                                       seconds=time[2])
        # the __str__() is becouse time is in seconds, and in this way 
        # return hh:mm:ss.ms
        profile[0].totaltime = totaltime.__str__()
        
        ## set fasted run
        speed = 0
        for run in runs.itervalues():
            if float(run[5]) > speed:
                profile[0].fastedrun = run[0]
                speed = run[5]
    else:
        profile[0].totaldistance = 0
        profile[0].totaltime = datetime.timedelta().__str__()
        profile[0].totalruns = 0
        profile[0].fastedrun = 0
    return


def showData(runner):
    """
    print the screen presentation
    """
    
    print '{0:<16} {1:^16} {2:>16}'.format("#" * 12, "Welcome..!", "#" * 12)
    print '{0:<16} {1:^16} {2:>16}'.format("#" * 12, \
                                           runner[0].name, "#" * 12)
    print ""
    print '{0:<16} {1:^16} {2:>16}'.format(" "*10, "#"*10, " "*10)
    print ""
    print '{0:<16} {1:^16} {2:>16}'.format(\
                                    ("Age: " + runner[0].age),\
                                    ("Weight: " + runner[0].weight),\
                                    ("Sex: " + runner[0].sex))
    print '{0:<16} {1:^16} {2:>16}'.format(\
                                    ("Total Distance :" + \
                                     str(runner[0].totaldistance)),\
                                  ("Total Time: " + str(runner[0].totaltime)),\
                                  ("Total Runs: " + str(runner[0].totalruns)))
    print '{0:<16} {1:^16} {2:>16}'.format(" "*10, \
                                   "Fasted Run: " + str(runner[0].fastedrun), \
                                   " "*10)
    print ""
    return


def loadActivity(runner):
    """
    return a list of istanced activity
    """
    # making a dictionary wiht the activities
    afile = open(runner[-1], "r")
    index = 0
    activities = {}
    for line in afile.readlines():
        if index < 2:
            # dont need the firsts 2 lines, its the basic info profile
            # and the column header
            index += 1
            continue
        activities[index -2] = line.split(",")
        index += 1
    afile.close()
    
    # making an instance of each activity
    for activitykey in activities.iterkeys():
        activities[activitykey] = Activity(runner, \
                                           activities[activitykey][0], \
                                           activities[activitykey][1], \
                                           activities[activitykey][2], \
                                           activities[activitykey][3])
    # return the list
    return activities.values()


def listActivities(activities, header=True):
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
                                                    activity.average_speed()
                                                    )
            print "{0:^3} : {1:^3}".format("c", "Back to main menu")
    else:
        print "No activities yet..."
    return


def timeInput():
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


def newGpxActivity(runner, activities):
    gpxfiles = readgpxfiles()
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
            select_option = int(raw_input("Introduce the number of the file: "))
            if select_option > len(gpxfiles):
                print "The Number sould be less than " + str(select_option) 
                pass
        except ValueError:
            print "Just Numbers..."
            pass
        break

    gpxactivity = GpxData(gpxfiles[select_option])
    gpxactivity.gpxParse()
    gpxactivity.totalDistance()
    gpxactivity.timeDate()
    
    # 0 for miles and 1 for kilometers
    pref = int(runner[0].pref)
    newactivity = Activity(runner, 
                           gpxactivity.getTInfo("date"), 
                           "R", 
                           gpxactivity.getTInfo("tdistance")[pref], 
                           gpxactivity.getTInfo("ttime"))
    
    newactivity.setP_and_AS()
    writeFile(runner, newactivity)
    activities.append(newactivity)
    return activities


def writeFile(runner, newactivity):
    afile = open(runner[-1], "a")
    afile_csv = csv.writer(afile)
    afile_csv.writerow([newactivity.date, 
                        newactivity.typerun, 
                        newactivity.distance, 
                        newactivity.time, 
                        newactivity.pace, 
                        newactivity.average_speed
                        ])
    afile.close()
    return

def newActivity(runner, activities):
    """
    Creates a new activity, append to the end of the file, instances and append
    to the list activities.
    Return activities list
    """
    date = raw_input("Introduce the date (dd/mm/yy): ")
    typerun = raw_input("Introduce the activity type 'R' for a race or 'T' for a trining session: ")
    distance = raw_input("Introduce the distance: ")
    time = timeInput() #function to input time
    # new instance
    newactivity = Activity(date, typerun, distance, time, runner)

    print "{:^}".format("=" * 20)
    listActivities([newactivity])
    
    # ask for confirmation, write the file if it's yes, if it's no makes a
    # recursive call, otherwise ask again.
    while True:
        isOkk= raw_input("Is this information is ok? (yes or no): ")
        if isOkk == "yes": 
            newactivity.setP_and_AS()
            writeFile(runner, newactivity)
            break # close the loop
        elif isOkk == "no":
            return newActivity(runner, activities)
        else:
            print "Just 'yes' or 'no'."
    activities.append(newactivity)
    return activities


def modActivity(runner, activities):
    """
    get an activity and mod the a data in the instance and file
    
    retruns an activites list moded
    """
    listActivities(activities)
    data_mod = ["Date", "Type", "Distance", "Time"]
    # loop to ask again if introduces a bad answer
    while True:
        selec_activity = raw_input("Introduce the number of the activity: ")
        if selec_activity in ["C", "c"]:
            return activities
        else:
            try:    
                int(selec_activity) 
            # In case introduce a wron string
            except ValueError: 
                print "Just Numbers from '0' to " + str(len(activities))
        
            if selec_activity > len(activities):
                pass
            else:
                actual_data= [activities[selec_activity].date, 
                              activities[selec_activity].typerun, 
                              activities[selec_activity].distance, 
                              activities[selec_activity].time]
    
                # Print a list of type data and data
                for adata in actual_data:
                    index = actual_data.index(adata)
                    print "{0:^5} {1:^5} {2:^5}".format(index, data_mod[index], adata)
                # loop to ask again if introduces a bad answer
                while True:
                    selec_data = raw_input("Introduce the number of the data: ")
                    if selec_data == "0":
                        new_data = raw_input("Introduce the new Date: ")
                        activities[selec_activity].date = new_data
                        break
                    elif selec_data == "1":
                        new_data = raw_input("Introduce the new Type Run: ")
                        activities[selec_activity].typerun = new_data
                        break
                    elif selec_data == "2":
                        new_data = raw_input("Introduce the new Distance: ")
                        activities[selec_activity].distance = new_data
                        activities[selec_activity].setP_and_AS()
                        break
                    elif selec_data == "3":
                        time = timeInput()
                        activities[selec_activity].time = time
                        activities[selec_activity].setP_and_AS()
                        break
            # the next two 'else' it is in case introduce an out of range index
                    else:
                        print "Just Numbers from '0' to '3'..."
        break

    # write the changes on the file and return the activites list
    return modFileActivity(runner, activities, selec_activity, todo="mod")


def delActivity(runner, activities):
    """
    select the activity to delete
    """
    listActivities(activities)
    while True:
        selec_activity = raw_input("Introduce the number of the activity: ")
        if selec_activity in ["C", "c"]:
            return activities
        else:
            try:
                int(selec_activity)
            except ValueError:  # In case get a string
                print "Just Numbers from '0' to " + str(len(activities))
            if selec_activity > len(activities):
                print "Just Numbers from '0' to " + str(len(activities))
                pass
        break
    return modFileActivity(runner, activities, selec_activity, todo="delete")

def modFileActivity(runner, activities, selec_activity, todo="mod", ):
    """
    This function write down the modification maked in the instance.
    todo=["mod", "delete")
    
    If delet an activity returns the activities list modified
    """
    # Adding 2 beacouse the file 1 line for the runner preference, and 1 for
    # the header for table of activities
    nline = 0
    if todo == "mod":
        for line in fileinput.input(runner[-1], inplace=True, mode="rb"):
            if nline == selec_activity + 2:
                line = activities[selec_activity].date + "," + \
                       activities[selec_activity].typerun + "," + \
                       activities[selec_activity].distance + "," + \
                       activities[selec_activity].time + "," + \
                       str(activities[selec_activity].pace) + "," + \
                       str(activities[selec_activity].average_speed)
                print line
                nline += 1
            else:
                line = line.replace("\n", "")
                print line
                nline +=1
    elif todo == "delete":
        for line in fileinput.input(runner[-1], inplace=True, mode="rb"):
            if nline == selec_activity + 2:
                del activities[selec_activity]
                nline += 1
                pass
            else:
                line = line.replace("\n", "")
                print line
                nline +=1
    return activities

def modRunner(runner):
    """
    modified the runner instance selected and the file
    """
    data = [runner[0].name, 
            runner[0].age, 
            runner[0].weight, 
            runner[0].sex, 
            runner[0].pref]
    
    for item in data:
        print "{0:^3} : {1:^3}".format(data.index(item), item)
    print "{0:^3} : {1:^3}".format("c", "Back to main menu")
    while True:
        selec_data = raw_input("Introduce the Number: ")

        if selec_data == "0":
            new_data = raw_input("Introduce the new Name: ")
            runner[0].name = new_data
            break
        elif selec_data == "1":
            new_data = raw_input("Introduce the new Age: ")
            runner[0].age = new_data
            break
        elif selec_data == "2":
            new_data = raw_input("Introduce the new Weight: ")
            runner[0].weight = new_data
            break
        elif selec_data == "3":
            new_data = raw_input("Introduce the new Sex: ")
            runner[0].sex = new_data
            break
        elif selec_data == "4":
            while True:
                new_data = raw_input("Introduce the new Preference '0' or '1': ")
                if new_data not in ["1", "0"]:
                        print "Just '0' or '1'"
                        pass                        
                break
            runner[0].pref = new_data
            break
        elif selec_data in ["c", "C"]:
            return
        else:
            print "Just Number from '0' to '4'...\n"
    # Writing the file
    nline = 0
    for line in fileinput.input(runner[-1], inplace=True, mode="rb"):
        if nline == 0:
            line = runner[0].name + "," + \
                    runner[0].age + "," + \
                    runner[0].weight + "," + \
                    runner[0].sex + "," + \
                    str(runner[0].pref)
            print line
            nline += 1
        else:
            line = line.replace("\n", "")
            print line
            nline += 1
    return


def mainAction():
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
    profiles_files = readProfiles()
    if len(profiles_files) == 0:
        print "Is this your first time?"
        newRunner()
        profiles_files = readProfiles()
    
    runners = loadRunners(profiles_files)
    sleep(1)
    print "LogIn...\n"
    runner = selectRunner(runners)
    print runner[0].totalruns
    setExtraInfo(runner)
    showData(runner)
    activities_list = loadActivity(runner)
    
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

        selec_option = raw_input("Whats you wants to do? \
(option Number): ")
        print "=" * 15
        print ""
        if selec_option == "0":
            listActivities(activities_list)
        elif selec_option == "1":
            while True:
                print "{0:^3} : {1:^3}".format("0", "Manual Entry")
                print "{0:^3} : {1:^3}".format("1", "GPX File")
                print "{0:^3} : {1:^3}".format("c", "Back to main menu")
                selec_option = raw_input("(option Number): ")
                if selec_option == "0":
                    activities_list = newActivity(runner, activities_list)
                    break
                elif selec_option == "1":
                    activities_list = newGpxActivity(runner, activities_list)
                    break
                elif selec_option in ["c", "C"]:
                    break
        elif selec_option == "2":
            activities_list = modActivity(runner, activities_list)
        elif selec_option == "3":
            activities_list = delActivity(runner, activities_list)
        elif selec_option == "4":
            modRunner(runner)
        elif selec_option == "5":
            print " Are you gonna run..?\n Have a nice Run!!!"
            break
        else:
            print "Nop, Just numbers from '0' to '5'...\n"
    return

if __name__ == '__main__':
    try:
        mainAction()
    except (KeyboardInterrupt, SystemExit):
        pass
