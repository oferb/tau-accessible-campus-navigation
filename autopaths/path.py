# a wrap for the path
# returns a json
# this class creates a new path obj using GH
import math


class Path:
    def __init__(self, path):
        self.path_from_graphhopper = path
        self.length = self.get_length()
        self.objects = self.get_objects()
        self.turns = self.get_turns()

    # get the total path length in km
    def get_length(self):
        length = (self.path_from_graphhopper['distance'] / 1000.0)
        return length

    # returns all the relevant for weighting objects as two dicts
    def get_objects(self):
        road = self.path_from_graphhopper['details']['road_class']
        road_dict = {}
        for i in range(len(road)):
            key = road[i][2]
            if key in road_dict:
                road_dict[key] = road_dict[key] + 1
            else:
                road_dict[key] = 1
        surface = self.path_from_graphhopper['details']['surface']
        surface_dict = {}
        i = 0
        for i in range(len(surface)):
            key = surface[i][2]
            if key != "paved" and key != "other":
                if key in surface_dict:
                    surface_dict[key] = surface_dict[key] + 1
                else:
                    surface_dict[key] = 1
        # print(surface_dict)
        return road_dict, surface_dict

    # returns an array summing the number of each turn's type on the path
    def get_turns(self):
        instructions = self.path_from_graphhopper['instructions']
        turns = [0] * 8
        for i in range(len(instructions)):
            turns[abs(int(instructions[i]['sign']))] += 1
        return turns

    def to_json(self):
        as_json = dict(self.__dict__)
        return as_json
