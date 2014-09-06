import os
import csv
import fileinput

c = 0
# remplace a data from a line
for line in fileinput.input("korrer.csv", inplace=True, mode="rb"):
    if c == 5:
        line = line.replace("\n", "").replace("9.9 Km", "9.91 Km")
        print line
    else:
        line = line.replace("\n", "")
        print line
        c +=1

# delete a line
for line in fileinput.input("korrer.csv", inplace=True, mode="rb"):
    if c == 3: 
        c += 1
        pass
        #print line[:-1]
    else:
        line = line.replace("\n", "")
        print line
        c +=1


print c

profiles_folder = "profiles/"

profiles = [(profiles_folder + afiles) for afiles in os.listdir(profiles_folder)]


K = open("profiles/r5.csv", "a")

