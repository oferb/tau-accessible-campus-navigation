from autostories.Section import Section
from autostories.OSMParser import create_nodes_info
from autostories.Section import Point
from autostories.ExampleInput import *
from autostories import CreateSectionsNew

PATH = "map2.osm"


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


def create_description(raw_points_list) -> list:
    """
    :param raw_points_list: [[lon,lat]] for every turn]
    :return: the text
    """
    if len(raw_points_list) == 0:
        return []
    result = []
    # points_list = get_all_nodes_in_route_simple(raw_points_list)
    points_list = create_points_list(raw_points_list)
    nodes_info = create_nodes_info(PATH)
    print("got until here")
    # section_list = split_to_sections(points_list, nodes_info)
    section_list = CreateSectionsNew.create_sections(points_list, nodes_info)
    print("len(section_list)", len(section_list), "\n")
    result.append(section_list[0].get_section_description(None))
    for section_index in range(1, len(section_list)):
        result.append(section_list[section_index].get_section_description(section_list[section_index - 1]))
    return result


if __name__ == '__main__':
    result = create_description(entrance_to_gilman_manual)
    for i in range(len(result)):
        print("\nsection:")
        print(result[i])


