import urllib.request
import json
import webbrowser
from path import *
import sys


# returns all paths between two coordinates
def generate_all_paths(lat1, lon1, lat2, lon2):
    url = "https://graphhopper.com/api/1/route?point=" + lon1 + "," + lat1 + "&point=" + lon2 + "," + lat2 + "&vehicle=foot&locale=he-IL&points_encoded=false&ch.disable=true&weighting=fastest&layer=Omniscale&key=172e5a82-96e0-4589-9496-cc22097511f3" + "&algorithm=alternative_route&ch.disable=true&alternative_route.max_paths=10&alternative_route.max_share_factor=10&alternative_route.max_weight_factor=10&details=surface&details=road_class&avoid=steps"
    print(url)
    text = urllib.request.urlopen(url).read()
    jsonL = json.loads(text)
    # print (jsonL)
    lists_of_paths = []
    for i in range(len(jsonL['paths'])):
        path = Path(jsonL['paths'][i])
        lists_of_paths.append(path)
    return lists_of_paths


# returns a coordinates array discribing the path object
def get_path_coordinates(path):
    return path.path_from_graphhopper['points']['coordinates']


# finds the optimal path in an array of path objects and returns it
def find_optimal(all_paths):
    path_min_index = 0
    min_weight = sys.maxsize
    for i in range(len(all_paths)):
        tmp_min = path_weight(all_paths[i])
        if tmp_min < min_weight:
            min_weight = tmp_min
            path_min_index = i
    return all_paths[path_min_index]


# calculates the total weight of an path object
def path_weight(path):
    return path_length_weight(path) + path_turns_weight(path) + path_objects_weight(path)


# returns the weight of the length of the path (weight=length in km)
def path_length_weight(path):
    len = path.length
    return len


# returns the weight of the turns of the path
def path_turns_weight(path):
    turns = path.turns
    turns_total_weight = 0
    for i in range(len(turns)):
        turns_total_weight += i * turns[
            i]  # TODO figure out what the exact turns data structure API and edit the code accordingly
    return turns_total_weight


# returns the combined weight of the objects in a specific path
# TODO define all the surfaces and sync with Reem's implementation
def path_objects_weight(path):
    objects_weight = 0
    single_object_weight = 0
    road_dict = path.objects[0]
    surface_dict = path.objects[1]

    for road in road_dict:
        if road == "FootWay":
            single_object_weight = 0
        elif road == "Living Street":
            single_object_weight = 5
        elif road == "Path":
            single_object_weight = 3
        elif road == "Pedestrians":
            single_object_weight = 5
        elif road == "Stairs":
            single_object_weight == 3
        elif road == "Service":
            single_object_weight = 6
        elif road == "unclassified":
            single_object_weight = 6
        else:
            single_object_weight = 0
        objects_weight += road_dict[road] * single_object_weight

        for surf in surface_dict:
            if surf == "Grass":
                single_object_weight = 6
            else:
                single_object_weight = 0
            objects_weight += surface_dict[surf] * single_object_weight

    return objects_weight

