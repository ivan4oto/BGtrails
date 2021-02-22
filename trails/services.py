from math import radians, cos, sin, asin, sqrt

from lxml import etree


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
            total_elevation += int(ele2) - int(ele1)
    return total_elevation

def strip_ns_prefix(tree):
    #xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    #for each element returned by the above xpath query...
    for element in tree.xpath(query):
        #replace element name with its local name
        element.tag = etree.QName(element).localname
    return tree

# f = open("/mnt/c/Users/ivan/Downloads/balkan_sky.gpx", "r")
# a = get_total_distance(f)
# b = get_total_elevation(f)
# c = get_starting_point(f)

# print(c)