from math import radians, cos, sin, asin, sqrt
import json

from lxml import etree
import matplotlib.path as mplPath
import numpy as np



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

def get_starting_point(gpx_file):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(gpx_file, parser)
    tree = strip_ns_prefix(tree)
    root = tree.getroot()
    for element in root.iter('trkpt'):
        if element.attrib.get('lat') and element.attrib.get('lon'):
            lat = element.attrib.get('lat')
            lon = element.attrib.get('lon')
    return (float(lat), float(lon),)


def get_total_distance(gpx_file):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(gpx_file, parser)
    tree = strip_ns_prefix(tree)
    root = tree.getroot()
    total_distance = 0
    elements_list = list(root.iter("trkpt"))
    for e in range(len(elements_list)-1):
        lat1, lon1 = float(elements_list[e].get('lat')), float(elements_list[e].get('lon'))
        lat2, lon2 = float(elements_list[e+1].get('lat')), float(elements_list[e+1].get('lon'))
        total_distance += haversine(lon1, lat1, lon2, lat2)
    return round(total_distance, 2)



def get_total_elevation(gpx_file):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(gpx_file, parser)
    tree = strip_ns_prefix(tree)
    root = tree.getroot()
    total_elevation = 0
    elements_list = list(root.iter("ele"))
    for e in range(len(elements_list)-1):
        ele1, ele2 = elements_list[e].text, elements_list[e+1].text
        if ele1 < ele2:
            total_elevation += int(float(ele2)) - int(float(ele1))
    return total_elevation

def strip_ns_prefix(tree):
    #xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    #for each element returned by the above xpath query...
    for element in tree.xpath(query):
        #replace element name with its local name
        element.tag = etree.QName(element).localname
    return tree

poly = [190, 50, 500, 310]
bbPath = mplPath.Path(np.array([[poly[0], poly[1]],
                     [poly[1], poly[2]],
                     [poly[2], poly[3]],
                     [poly[3], poly[0]]]))

bbPath.contains_point((200, 100))


mountain_dict = {
    "Stara Planina": '../cdn_test/media/polygons/stara_planina.json'
}
point = (24.669800, 42.514626)


def localise_point(point, mountain_dict):
    for location_name, file_path in mountain_dict.items():
        with open(file_path, encoding='utf-8-sig') as f:
            jsonfile = json.load(f)
            polygon = jsonfile.get('polygon')
            polyPath = mplPath.Path(np.array(polygon))
            if polyPath.contains_point(point):
                return jsonfile.get('name')