from osmread import parse_file, Node, Way
from autostories.Section import Point
import pprint
from collections import namedtuple



def osm_to_entities(path: str):
    entities = []
    for entity in parse_file(path):
        entities.append(entity)
    return entities


def create_nodes(entities):
    nodes = []
    for entity in entities:
        if isinstance(entity, Node):
            # node = OSMNode(entity.id, entity.lon, entity.lat)
            nodes.append(entity)
    return nodes


def create_ways(entities):
    ways = []
    for entity in entities:
        if isinstance(entity, Way):
            # way = OSMWay(entity.id, entity.nodes)
            ways.append(entity)
    return ways


def create_output_list(nodes, ways):
    output = []

    for i, item in enumerate(nodes):
        node_tags = {}
        start_point = Point(item.lat, item.lon, item.id)
        node_tags["start_point"] = start_point

        if "highway" in item.tags:
            node_tags["comments"] = item.tags["highway"]

        # TODO
        # if "amenity" in item.tags:
        #    node_tags["r_side_description"] = item.tags["amenity"]

        if "barrier" in item.tags:
            node_tags["barrier"] = item.tags["barrier"]

        for way in ways:
            if item.id in way.nodes:

                # write way highway-type
                if "highway" in way.tags:
                    node_tags["ground_type"] = way.tags["highway"]
                    if way.tags["highway"] == "steps":
                        node_tags["is_steps"] = True
                    else:
                        node_tags["is_steps"] = False

                # write way handrail
                if "handrail" in way.tags:
                    node_tags["rail"] = way.tags["handrail"]

                # write way step-count
                if "step_count" in way.tags:
                    node_tags["steps_num"] = way.tags["step_count"]

                # write way barrier
                if "barrier" in way.tags:
                    node_tags["barrier"] = way.tags["barrier"]

                # write way name
                if "name:en" in way.tags:
                    node_tags["name"] = way.tags["name:en"]

        output.append(node_tags)

    for way in ways:
        node_ids = way.nodes
        for id in node_ids:
            node_tags = {}
            current_node = None
            for node in nodes:
                if (node.id == id) and node.tags:
                    current_node = node
                    break
            if current_node is not None:
                start_point = Point(current_node.lat, current_node.lon, id)  # ???
                node_tags["start_point"] = start_point

                if "highway" in way.tags:
                    node_tags["ground_type"] = way.tags["highway"]
                    if way.tags["highway"] == "steps":
                        node_tags["is_steps"] = True
                    else:
                        node_tags["is_steps"] = False

                # write way handrail
                if "handrail" in way.tags:
                    node_tags["rail"] = way.tags["handrail"]

                # write way step-count
                if "step_count" in way.tags:
                    node_tags["steps_num"] = way.tags["step_count"]

                # write way barrier
                if "barrier" in way.tags:
                    node_tags["barrier"] = way.tags["barrier"]

                # write way name

                if "name:en" in way.tags:
                    node_tags["name"] = way.tags["name:en"]
                # TODO
                # if "amenity" in way.tags:
                #    node_tags["r_side_description"] = way.tags["amenity"]
            if node_tags:
                output.append(node_tags)
    return output


def write_nodes_to_file(nodes, name, sheet, book):
    for i, node in enumerate(nodes):
        cell = "A" + str(i)
        print(str(node.id))
        print(sheet[cell])
        sheet[cell] = str(node.id)
    book.save(name)


def create_nodes_info(path: str):
    entities = osm_to_entities(path)
    nodes = create_nodes(entities)
    ways = create_ways(entities)
    return create_output_list(nodes, ways)


def example_look_for_steps():
    nodes_info = create_nodes_info("part_map_entrance_to_gilman.osm")
    for node in nodes_info:
        if "is_steps" in node and node["is_steps"]:
            pprint.pprint(node)
            print(node["start_point"].to_string())
    print(len(nodes_info))


if __name__ == '__main__':
    example_look_for_steps()
