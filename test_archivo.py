import os
# import csv
import fileinput
import sqlite3
from xml.etree import ElementTree
from math import radians, cos, sin, asin, sqrt


# get coneccion with db
conn = sqlite3.Connection("runner.db")
cur = conn.cursor()

# excecute
cur.execute("""create table runner (
name text(50),
age integer(2))""")
cur.execute('insert into runner values ("koxmoz","2")')

# get data
a = cur.execute("""select * from runner""")
for row in a.fetchall():
    name, age = row
    print name, age

# close and commit
cur.close()
conn.commit()
conn.close()

# define variables froma a list
z = (1, 2, 3)
a, b, c = z
print a, b, c

with open('gradual.gpx', 'rt') as f:
    tree = ElementTree.parse(f)

for item in tree.getiterator():
    if "trkpt" in item.__str__():
        print item

# funciona igual con el time
for item in tree.getiterator():
    if "ele" in item.__str__():
        item.text
# obtiene latitud y longitud,
for node in tree.iter('{http://www.topografix.com/GPX/1/1}trkpt'):
    lat = node.attrib.get("lat")
    lon = node.attrib.get("lon")
    print lat, lon


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    km = 6367 * c
    # in miles
    ml = 3956 * c
    return km, ml

c = 0
# remplace a data from a line
for line in fileinput.input("korrer.csv", inplace=True, mode="rb"):
    if c == 5:
        line = line.replace("\n", "").replace("9.9 Km", "9.91 Km")
        print line
    else:
        line = line.replace("\n", "")
        print line
        c += 1

# delete a line
for line in fileinput.input("korrer.csv", inplace=True, mode="rb"):
    if c == 3:
        c += 1
        pass
        # print line[:-1]
    else:
        line = line.replace("\n", "")
        print line
        c += 1


print c

profiles_folder = "profiles/"

profiles = [(profiles_folder + afiles)
            for afiles in os.listdir(profiles_folder)]


K = open("profiles/r5.csv", "a")
