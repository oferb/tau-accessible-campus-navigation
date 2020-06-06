import urllib.request
import bs4
import time
from autostories.Section import Point
from autostories.ExampleInput import *
import math


def get_boundaries_box(lat, lon, meters):
    latmeters = 10 ** 8 / 899.0
    lonmeters = 10 ** 8 / 1268.0
    min_x, min_y = (lat - meters / latmeters, lon - meters / lonmeters)
    max_x, max_y = (lat + meters / latmeters, lon + meters / lonmeters)
    return (min_x, min_y), (max_x, max_y)


def get_interesting_points(lat, lon, meters):
    l = []
    (lat1, lon1), (lat2, lon2) = get_boundaries_box(lat, lon, meters)
    url = "http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s" % (lon1, lat1, lon2, lat2)

    osm_text = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(osm_text, features="lxml")
    nodes = soup.findAll("node")
    points = []
    for node in nodes:
        name_tag = node.find("tag")  # attrs={'k': 'name'})
        if name_tag:
            lat = float(node.get("lat"))
            lon = float(node.get("lon"))
            name = name_tag.get("v")
            timestamp = int(time.time())
            points.append(node)
    return points


def get_points_between_two_points(point1, point2):
    (lat1, lon1), (lat2, lon2) = (point1.lat, point1.lon), (point2.lat, point2.lon)
    url = "http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s" % (
        min(lon1, lon2), min(lat1, lat2), max(lon1, lon2), max(lat1, lat2))
    osm_text = urllib.request.urlopen(url).read()

    soup = bs4.BeautifulSoup(osm_text, "lxml")
    print(soup)
    # print( soup")
    # print(soup)
    nodes = soup.findAll("node")
    print(len(nodes))
    points = []
    for node in nodes:  # 1184053312
        # print("next node:")
        # print(node)
        # print("\n\n\n")
        name_tag = node.find("tag")  # attrs={'k': 'name'})
        # print("name_tag",name_tag)
        if name_tag:
            lat = float(node.get("lat"))
            lon = float(node.get("lon"))
            name = name_tag.get("v")
            # print("name",name)
            # print(node.get("uid"))
            timestamp = int(time.time())
            points.append(Point(lat, lon, node.get("uid")))
    return points


def is_on_line(point1, point2, lat, lon):
    # m1 = (lat - point1.lat) / (lon - point1.lon)
    # m2 = (lat - point2.lat) / (lon - point2.lon)
    # if m1 == m2:
    #    print("exacly on line")
    point12dis = Point.calc_distance(point1, point2)

    tempPoint = Point(lat, lon, -1)
    a = Point.calc_distance(point1, tempPoint) + Point.calc_distance(tempPoint, point2)
    if (abs(point12dis - a) < 0.00001):
        return True
    return False


def get_points_between_two_points_second_version(point1, point2):
    (lat1, lon1), (lat2, lon2) = (point1.lat, point1.lon), (point2.lat, point2.lon)
    url = "http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s" % (
        min(lon1, lon2), min(lat1, lat2), max(lon1, lon2), max(lat1, lat2))
    osm_text = urllib.request.urlopen(url).read()

    soup = bs4.BeautifulSoup(osm_text, "lxml")
    nodes = soup.findAll("node")
    # print("len(nodes)",len(nodes))
    points = []
    for node in nodes:  # 1184053312
        lat = float(node.get("lat"))
        lon = float(node.get("lon"))

        if is_on_line(point1, point2, lat, lon):
            points.append(Point(lat, lon, node.get("id")))
    return points


def point_node_distance(point1, node1):
    p_lat = point1[1]
    p_lon = point1[0]
    n_lat = float(node1.get("lat"))
    n_lon = float(node1.get("lon"))
    return math.sqrt((p_lat - n_lat) ** 2 + (p_lon - n_lon) ** 2)


def get_closest_node(point1):
    nodes = get_interesting_points(point1[1], point1[0], 5);
    if not nodes:
        return -1
    max = 1000  # impossible distance between coordinates as max
    max_node = 0
    dist = 0
    for node in nodes:
        dist = point_node_distance(point1, node)
        if (dist < max):
            max = dist
            max_node = node
    return max_node.get("uid")


# points = Section.Point.create_points_list([[32.113254, 34.802280,7404723491]])
# print(get_closest_node(points[0]))
# print(get_interesting_points(32.112123, 34.803953,20))
if __name__ == '__main__':
    first = entrance_to_gilman[1]
    second = entrance_to_gilman[2]
    firstPoint = Point(first[1], first[0], -1)
    secondPoint = Point(second[1], second[0], -1)

    res = get_points_between_two_points_second_version(firstPoint, secondPoint)
    for i in res:
        print(i.to_string())
    """
    for i in range(len(entrance_to_gilman) - 1):
        print("current i", i)
        first = entrance_to_gilman[i]
        second = entrance_to_gilman[i+1]
        firstPoint = Point(first[1], first[0], -1)
        secondPoint = Point(second[1], second[0], -1)

        res = get_points_between_two_points_second_version(firstPoint,secondPoint)
        if(len(res) > 0):
            print(len(res))
"""
