# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 22:02:52 2014

@author: koxmoz
"""

from xml.etree import ElementTree
from math import radians, cos, sin, asin, sqrt
import datetime
from os import listdir

GPX_FILE = "gpxfiles/"

class GpxData(object):
    def __init__(self, afile_dir):
        self.RawData = {"lat": [], "lon": [], "ele": [], "time": []}
        self.TInfo = {"tdistance": None, "ttime": None, "date": None}
        self.afile_dir = afile_dir
    
    def setRawData(self, key, value):
        if self.RawData.has_key(key):
            self.RawData[key].append(value)
    def setTInfo(self, key, value):
        if self.TInfo.has_key(key):
            self.TInfo[key] = value
    
    def getRawData(self, key):
        if self.RawData.has_key(key):
            return self.RawData[key]
    def getTInfo(self, key):
        if self.TInfo.has_key(key):
            return self.TInfo[key]

    def haversine(self, lon1, lat1, lon2, lat2):
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
        return [ml, km]

    def gpxParse(self):
        with open(self.afile_dir, 'rt') as gpx_file:
            gpx = ElementTree.parse(gpx_file)
        gpx_file.close()
        
        for point in gpx.getiterator():
            if "trkpt" in point.__str__():
                self.setRawData("lat", point.attrib.get("lat"))
                self.setRawData("lon", point.attrib.get("lon"))
            for info in point.getiterator():
                if "ele" in info.__str__():
                    self.setRawData("ele", info.text)
                elif "time" in info.__str__():
                    self.setRawData("time", info.text)
        # the first pint has no elevation
        del self.RawData["lat"][0]
        del self.RawData["lon"][0]
        del self.RawData["time"][0]

    def totalDistance(self):
        total_distance = [0, 0]
        try:
            for index in range(len(self.RawData["lat"])):
                lat1 = self.RawData["lat"][index]
                lat2 = self.RawData["lat"][index + 1]
                lon1 = self.RawData["lon"][index]
                lon2 = self.RawData["lon"][index + 1]
                tmp_distance = self.haversine(float(lon1), 
                                              float(lat1), 
                                              float(lon2), 
                                              float(lat2))
                total_distance[0] = total_distance[0] + tmp_distance[0] # km
                total_distance[1] = total_distance[1] + tmp_distance[1] # ml
        except IndexError:
            pass
        # set Total Distance
        total_distance[0] = round(total_distance[0], 2)
        total_distance[1] = round(total_distance[1], 2)
        self.setTInfo("tdistance", total_distance)
    
    def timeDate(self):
        def dateToTime(completedate):
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
        initial_time = dateToTime(self.RawData["time"][0])
        final_time = dateToTime(self.RawData["time"][-1])

        # set total time
        total_time = final_time - initial_time
        self.setTInfo("ttime", total_time.__str__())
        # set date
        date = self.RawData["time"][0].replace("Z", "").split("T")[0]
        self.setTInfo("date", date)

def readgpxfiles():
    """ 
    Read the files in the profile folder and return a list of profile    
    """
    # I'm not shure how clear is this 
    gpxfiles = [(GPX_FILE + afiles) \
                    for afiles in listdir(GPX_FILE)]
    return gpxfiles

