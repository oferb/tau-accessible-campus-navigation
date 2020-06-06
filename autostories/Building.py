from autostories.Section import Section
from autostories.OSMParser import create_nodes_info
from autostories.Section import Point
from autostories.TwoPoints import get_points_between_two_points, get_points_between_two_points_second_version
from autostories.ExampleInput import *
from autostories.create_sections_new import create_sections
PATH = "map2.osm"


def get_empty_node_info(point):
    result = {"start_point": point, "is_steps": False, "ground_type": "UnKnown"}
    return result


def fetch_point_info(point, nodes_info):
    for item in nodes_info:
        # if node is in nodes
        if item["start_point"].id == point.id:
            info = item
            if info["start_point"].lon == 0 and info["start_point"].lat == 0:
                info["start_point"].lon = point.lon
                info["start_point"].lat = point.lat
            return info
    return get_empty_node_info(point)


def get_right_desc(point):
    '''
    fetch other points from OSM to describe right side
    :return:
    '''
    pass


def get_left_desc(point):
    '''
    fetch other points from OSM to describe left side
    :return:
    '''
    pass


def get_end_point():
    return Point(0, 0, 0)

def create_section_from_info(info):
    section = Section(info["start_point"], get_end_point(), info["is_steps"], 0, info["ground_type"])
    if "steps_num" in info.keys():
        section.steps_num = info["steps_num"]
    if "rail" in info.keys():
        section.rail = info["rail"]
    return section


def create_points_list(raw_points_list):
    """

    :param points_list: len >= 1
    :return:
    """
    new_points_list = []

    for point_index in range(0, len(raw_points_list)):
        # closest_point = get_closest_node(points_list[point_index])
        new_points_list.append(Point(raw_points_list[point_index][1], raw_points_list[point_index][0], -1))

    return new_points_list


def get_all_nodes_in_route(points_list):
    points_list = create_points_list(points_list)
    all_points = []
    points_id_set = set()  # TODO - i did not understand why we need the del, because its wrong (for example if
    # TODO - len(points_to_add_list) = 0), so i did something else that is 100% correct but longer, can rewrite if you want and
    # TODO - sure it will work
    for i in range(0, len(points_list) - 1):
        points_to_add_list = get_points_between_two_points(points_list[i], points_list[i + 1])
        for point_to_add in points_to_add_list:
            if point_to_add.id not in points_id_set:
                points_id_set.add(point_to_add.id)
            else:
                points_to_add_list.remove(point_to_add)
        all_points.extend(points_to_add_list)
        print(len(all_points))
    return all_points


def get_all_nodes_in_route_simple(raw_points_list):
    points_list = create_points_list(raw_points_list)
    print("start points_list len", len(points_list))
    for i in range(0, len(points_list) - 2):
        points_to_add_list = get_points_between_two_points_second_version(points_list[i], points_list[i + 1])
        # print(i, " to ", i+1, " add: ", len(points_to_add_list))
        points_list.extend(points_to_add_list)
    print("end points_list len", len(points_list))
    return points_list


def split_to_sections(points_list, nodes_info) -> list:
    """

    :param points_list: list of points of type Point (from Section)

    :return list of sections, such that each geographical parameter is valid to all of it
    """
    sections = []

    start = points_list[0]
    info = fetch_point_info(start, nodes_info)
    sec = create_section_from_info(info)
    sections.append(sec)

    for point in points_list[1:]:
        info = fetch_point_info(point, nodes_info)
        if info:
            next_sec = create_section_from_info(info)
            if Section.check_if_dff(sec, next_sec):
                sections.append(next_sec)
            sec = next_sec

    start_sec = sections[0]
    for section in sections[1:]:
        end_sec = section
        start_sec.end_point = end_sec.start_point
        start_sec.length = Point.calc_distance(start_sec.start_point, start_sec.end_point)
        start_sec = end_sec

    return sections


def create_description(raw_points_list) -> str:
    """
    :param raw_points_list: [[lon,lat]] for every turn]
    :return: the text
    """
    if len(raw_points_list) == 0:
        return ""
    result = ""
    points_list = get_all_nodes_in_route_simple(raw_points_list)
    nodes_info = create_nodes_info(PATH)

    #section_list = split_to_sections(points_list, nodes_info)
    section_list = create_sections(points_list,nodes_info)
    result += section_list[0].get_section_description(None)
    for section_index in range(1, len(section_list)):
        result += section_list[section_index].get_section_description(section_list[section_index - 1])

    return result


if __name__ == '__main__':
    print(create_description(entrance_to_gilman))
