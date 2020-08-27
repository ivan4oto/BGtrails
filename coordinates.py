import sys
from math import radians, cos, sin, asin, sqrt
import geopy.distance
import gpxpy
import gpxpy.gpx
import os
from glob import glob


def get_location(gpxdata):
    piece = gpxdata.split('<')
    for p in piece:
        if p.startswith('trkpt'):
            p = p.split('"')
            lat, long = float(p[1]), float(p[-2])
            return (lat, long)


def get_distance(user_coords, trail_coords):
    return geopy.distance.vincenty(user_coords, trail_coords).km


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
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_track_length(gpxtrack):
    # gpxtrack.decode()
    gpx = gpxpy.parse(gpxtrack)
    ele = 0
    dist = 0

    for track in gpx.tracks:
        for segment in track.segments:
            for i in range(len(segment.points)-2):
                pointA = segment.points[i]
                pointB = segment.points[i+1]
                dist += haversine(pointA.longitude, pointA.latitude, pointB.longitude, pointB.latitude)
                try:
                    if pointA.elevation > pointB.elevation:
                        ele += pointA.elevation - pointB.elevation
                except TypeError:
                    continue

    dist = int(dist)
    ele = int(ele)
    print(dist, ele)

    return (dist, ele)


def main():
    with open('media/ASR_2017_26.08.17.gpx', 'r') as f:
        print(type(get_location(f)[0]))


if __name__ == "__main__":
    main()
