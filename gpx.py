# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 22:02:52 2014

@author: koxmoz

This program is GPL v3, read the LICENSE file.
"""

from xml.etree import ElementTree
from math import radians, cos, sin, asin, sqrt
import datetime
from os import listdir

GPX_FILE = "gpxfiles/"


class Gpx_Data(object):
    """
    a class for parse the GPX file, and get in a dictionary, total distance,
    total time, date, pace, speed, and also get in another dictionary the
    latitude, longitude and elevation for future proposits
    """
    def __init__(self, afile_dir):
        self.raw_data = {"lat": [], "lon": [], "ele": [], "time": []}
        self.total_info = {"tdistance": None, "ttime": None, "date": None,
                           "pace": None, "speed": None}
        self.afile_dir = afile_dir

    def set_raw_data(self, key, value):
        """
        set new info in raw_data
        """
        if key in self.raw_data:
            self.raw_data[key].append(value)

    def set_total_info(self, key, value):
        """
        set new info in total_info
        """
        if key in self.total_info:
            self.total_info[key] = value

    def getraw_data(self, key):
        """
        get info from raw_data
        """
        if key in self.raw_data:
            return self.raw_data[key]

    def gettotal_info(self, key):
        """
        get info from total_info
        """
        if key in self.total_info:
            return self.total_info[key]

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points on the earth
        (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        h_a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        h_c = 2 * asin(sqrt(h_a))

        # 6367 km is the radius of the Earth
        km = 6367 * h_c
        # in miles
        ml = 3956 * h_c
        return [ml, km]

    def gpx_parse(self):
        """
        examine the root to find <trkpt> (track point) and get lat and lon.
        and the <ele> have the elevation. The same for <time>.
        """
        with open(self.afile_dir, 'rt') as gpx_file:
            gpx = ElementTree.parse(gpx_file)
        gpx_file.close()

        for point in gpx.getiterator():
            if "trkpt" in point.__str__():
                self.set_raw_data("lat", point.attrib.get("lat"))
                self.set_raw_data("lon", point.attrib.get("lon"))
            for info in point.getiterator():
                if "ele" in info.__str__():
                    self.set_raw_data("ele", info.text)
                elif "time" in info.__str__():
                    self.set_raw_data("time", info.text)
        # the first point has no elevation
        del self.raw_data["lat"][0]
        del self.raw_data["lon"][0]
        del self.raw_data["time"][0]

    def total_distance(self):
        """
        set the initial distance in 0, then get the distance betwin two points
        and add  it. like in haversine metod, the first element on the list is
        in miles, the second in kilometers.
        """
        total_dist = [0, 0]
        try:
            for index in range(len(self.raw_data["lat"])):
                lat1 = self.raw_data["lat"][index]
                lat2 = self.raw_data["lat"][index + 1]
                lon1 = self.raw_data["lon"][index]
                lon2 = self.raw_data["lon"][index + 1]
                tmp_distance = self.haversine(float(lon1),
                                              float(lat1),
                                              float(lon2),
                                              float(lat2))
                total_dist[0] = total_dist[0] + tmp_distance[0]  # km
                total_dist[1] = total_dist[1] + tmp_distance[1]  # ml
        except IndexError:
            pass
        # set Total Distance
        total_dist[0] = round(total_dist[0], 2)
        total_dist[1] = round(total_dist[1], 2)
        self.set_total_info("tdistance", total_dist)

    def time_date(self):
        """
        convert the string time to a datetime object, and get the diference
        betwin final time and the initial time.
        """
        def date_to_time(completedate):
            """
            string to datetime object
            """
            # convert "2014-08-29T19:47:11Z" to ["2014-08-29", "19:47:11"] and
            # get the last one "19:47:11"
            time = completedate.replace("Z", "").split("T")[1]
            # convert "19:47:11" to ["19", "47", "11"] hours, minutes, seconds
            time = time.split(":")
            # convert to datetime type
            time = datetime.timedelta(hours=int(time[0]),
                                      minutes=int(time[1]),
                                      seconds=float(time[2]))
            return time
        initial_time = date_to_time(self.raw_data["time"][0])
        final_time = date_to_time(self.raw_data["time"][-1])

        # set total time
        total_time = final_time - initial_time
        self.set_total_info("ttime", total_time.__str__())
        # set date
        date = self.raw_data["time"][0].replace("Z", "").split("T")[0]
        self.set_total_info("date", date)
        return

    def pace_and_speed(self, pref):
        """
        sets pace and average speed. need the preferences of the runner to
        select the correct distance.
        """
        time = [float(x) for x in self.total_info["ttime"].split(":")]
        time = datetime.timedelta(hours=time[0], minutes=time[1],
                                  seconds=time[2])
        self.total_info["pace"] = round((time.total_seconds() / 60) / float(self.total_info["tdistance"][pref]), 2)
        self.total_info["speed"] = round(float(self.total_info["tdistance"][pref]) / (time.total_seconds() / 3600), 2)
        return


def read_gpx_files():
    """
    Read the files in the profile folder and return a list of profile
    """
    # I'm not shure how clear is this
    gpxfiles = [(GPX_FILE + afiles)
                for afiles in listdir(GPX_FILE)]
    return gpxfiles
