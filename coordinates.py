import sys
import geopy.distance


def get_location(gpxdata):
    piece = gpxdata.split('<')
    for p in piece:
        if p.startswith('trkpt'):
            p = p.split('"')
            lat, long = float(p[1]), float(p[-2])
            return (lat, long)


def get_distance(user_coords, trail_coords):
    return geopy.distance.vincenty(user_coords, trail_coords).km


def main():
    pass


if __name__ == "__main__":
    pass