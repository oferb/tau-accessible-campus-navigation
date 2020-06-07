from autostories.Section import Section
from autostories.GetPointsBySegment import get_points_between_two_points_by_segment_distance
from autostories.Section import Point


def create_empty_sections(points_list: list) -> list:
    sections = []
    for i in range(len(points_list) - 1):
        sections.append(Section(points_list[i], points_list[i + 1]))
    return sections


def node_is_nodes_list(node_list, node):
    for i in range(len(node_list)):
        if node_list[i]["start_point"].equal(node["start_point"]):
            return True
    return False


def remove_by_id(current_nodes: list, node):
    index_to_remove = -1
    for i in range(len(current_nodes)):
        if current_nodes[i]["start_point"].equal(node["start_point"]):
            index_to_remove = i
            break
    if index_to_remove != -1:
        del current_nodes[index_to_remove]


def divide_the_nodes(prev_section: Section, prev_nodes: list, current_section: Section, current_nodes: list):
    result_current_nodes = current_nodes.copy()
    result_prev_nodes = prev_nodes.copy()
    for i in range(len(prev_nodes)):
        current_shared_node = prev_nodes[i]
        if node_is_nodes_list(result_current_nodes, current_shared_node):
            if Point.calc_distance(prev_section.start_point, current_shared_node["start_point"]) < Point.calc_distance(
                    current_shared_node["start_point"], current_section.end_point):
                remove_by_id(result_current_nodes, current_shared_node)
            else:
                remove_by_id(result_prev_nodes, current_shared_node)
    return result_prev_nodes, result_current_nodes


def create_nodes_to_add_to_sections(sections, nodes_info):
    nodes_to_add_to_sections = [get_points_between_two_points_by_segment_distance(nodes_info, sections[0].start_point,
                                                                                  sections[0].end_point)]

    for i in range(1, len(sections)):
        nodes_to_add_to_sections.append(
            get_points_between_two_points_by_segment_distance(nodes_info, sections[i].start_point,
                                                              sections[i].end_point))
        result_prev_nodes, result_current_nodes = divide_the_nodes(sections[i - 1], nodes_to_add_to_sections[-2],
                                                                   sections[i], nodes_to_add_to_sections[-1])
        nodes_to_add_to_sections[-2] = result_prev_nodes
        nodes_to_add_to_sections[-1] = result_current_nodes
    return nodes_to_add_to_sections


# TODO add handle changes
def add_parameters_to_section_by_nodes(section, nodes_to_section):
    result_sections = []
    length = Point.calc_distance(section.start_point, section.end_point)
    is_steps = False
    ground_type: str = ""
    slope: int = 0
    r_side_description: str = ""
    l_side_description: str = ""
    steps_num: int = 0
    rail: str = "N"
    stairs_slope: str = "N"
    block: str = ""
    comments: str = ""
    name: str = ""
    start_point = section.start_point
    end_point = section.end_point
    for i in range(len(nodes_to_section)):
        current_node = nodes_to_section[i]
        if "is_steps" in current_node:
            is_steps = current_node["is_steps"]
        if "ground_type" in current_node:
            ground_type = current_node["ground_type"]

        if "slope" in current_node:
            slope = current_node["slope"]
        if "r_side_description" in current_node:
            r_side_description = current_node["l_side_description"]
        if "l_side_description" in current_node:
            l_side_description = current_node["l_side_description"]
        if "steps_num" in current_node:
            steps_num = current_node["steps_num"]
        if "rail" in current_node:
            rail = current_node["rail"]
        if "stairs_slope" in current_node:
            stairs_slope = current_node["stairs_slope"]
        if "block" in current_node:
            block = current_node["block"]
        if "comments" in current_node:
            comments = current_node["comments"]
        if "name" in current_node:
            name = current_node["name"]
    end_section: Section = Section(start_point, end_point)
    end_section.set_parameters(is_steps, length, ground_type, slope, r_side_description, l_side_description, steps_num,
                               rail, stairs_slope, block, comments, name)
    result_sections.append(end_section)
    return result_sections


def create_sections(points_list, nodes_info) -> list:
    """

    :param points_list: list of points of type Point (from Section)

    :return list of sections, such that each geographical parameter is valid to all of it
    """
    sections = create_empty_sections(points_list)
    nodes_to_add_to_sections = create_nodes_to_add_to_sections(sections, nodes_info)
    result_sections = []
    for i in range(len(sections)):
        result_sections.extend(add_parameters_to_section_by_nodes(sections[i], nodes_to_add_to_sections[i]))
    return result_sections
