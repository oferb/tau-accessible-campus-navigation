import numpy as np
import math

# radius of the Earth
R = 6373.0


class Point:
    def __init__(self, lat, lon, id):
        self.lat = lat
        self.lon = lon
        self.id = id

    def to_string(self):
        return "lat:" + str(self.lat) + "\t" + str(self.lon) + "\t" + str(self.id)

    def get_angle(self, other_point):
        dlon = self.lon - other_point.lon
        y = math.sin(dlon) * math.cos(other_point.lat)
        x = math.cos(self.lat) * math.sin(other_point.lat) - math.sin(self.lat) * math.cos(other_point.lat) * math.cos(
            dlon)
        brng = math.atan2(y, x)
        brng = math.degrees(brng)
        brng = (brng + 360) % 360
        return brng

    def get_x_y(self):
        """Convert angluar to cartesian coordiantes

        latitude is the 90deg - zenith angle in range [-90;90]
        lonitude is the azimuthal angle in range [-180;180]
        """
        r = 6371  # https://en.wikipedia.org/wiki/Earth_radius
        theta = math.pi / 2 - math.radians(self.lat)
        phi = math.radians(self.lon)
        x = r * math.sin(theta) * math.cos(phi)  # bronstein (3.381a)
        y = r * math.sin(theta) * math.sin(phi)
        return [x, y]

    @staticmethod
    def sub_points(point1, point2):
        return Point(point2.lat - point1.lat, point2.lon - point1.lon, 0)

    @staticmethod
    def calc_distance(point1, point2):
        lat1 = math.radians(point1.lat)
        lon1 = math.radians(point1.lon)
        lat2 = math.radians(point2.lat)
        lon2 = math.radians(point2.lon)

        dlon = lon2 - lon1

        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        distance = distance * 1000  # to meter

        return distance


class Section:
    def __init__(self, start_point: Point, end_point: Point, is_steps: bool, length: int, ground_type: str = "",
                 slope: int = 0,
                 r_side_description: str = "", l_side_description: str = "",
                 steps_num: int = 0, rail: str = "N", stairs_slope: str = "N", block: str = "", comments: str = "",
                 name=""):
        """
        :param rail: out of (N - no rail, "left","right")
        :param stairs_slope: out of ("N" - no stairs,"up","down")
        :param comments: no stairs comments
        """

        self.start_point = start_point  # 0
        self.end_point = end_point  # 1
        self.is_steps = is_steps  # 2
        self.length = length  # 3
        self.ground_type = ground_type  # 4
        self.slope = slope  # 5
        self.r_side_description = r_side_description  # 6
        self.l_side_description = l_side_description  # 7
        self.steps_num = steps_num  # 8
        self.rail = rail  # 9
        self.stairs_slope = stairs_slope  # 10
        self.block = block  # 11
        self.comments = comments  # 12
        self.name = name  # 13

    @staticmethod
    def check_if_dff(section1, section2):
        types_diff = (section1.ground_type != section2.ground_type) or (section1.is_steps != section2.is_steps)
        angle_diff = section1.start_point.get_angle(section1.end_point) != section2.start_point.get_angle(
            section2.end_point)
        return types_diff or angle_diff  # TODO

    def create_turn_description(self, prev_angle) -> str:

        turn_angle = self.angle - prev_angle
        if turn_angle > 180:
            turn_angle = 360 - turn_angle
            direction = "left"
        elif 0 < turn_angle <= 180:
            direction = "right"
        elif -180 < turn_angle < 0:
            turn_angle *= -1
            direction = "left"
        else:  # turn_angle < -180
            turn_angle += 360
            direction = "right"
        turn_angle = turn_angle // 1
        if turn_angle > 30:
            return "turn " + str(turn_angle) + " degrees " + direction + "\n"
        return ""

    def create_ground_type_description(self) -> str:
        return "the ground type is " + str(self.ground_type)

    def create_slope_description(self) -> str:
        return "there is a slope, and the angle is " + str(self.slope)

    def create_steps_description(self) -> str:
        result = "go " + self.stairs_slope + " " + str(self.steps_num) + " stairs"
        if self.rail != "N":
            result += ", use the rail on the " + self.rail
        return result

    def create_r_side_description(self) -> str:
        return "in your right side you can find " + self.r_side_description

    def create_l_side_description(self) -> str:
        return "in your left side you can find " + self.l_side_description

    def create_length_description(self) -> str:
        return "the length of the road is " + str(self.length)

    def create_block_description(self) -> str:
        return "there is a blocking object ahead: " + self.block

    def create_comments_description(self) -> str:
        return "here is some extra information about your road " + self.comments

    def create_name_description(self) -> str:
        return "the name of the road is: " + self.name

    def get_section_description(self, prev_section=None):
        result = ""
        self.angle = self.start_point.get_angle(self.end_point)
        # if prev_section is not None and self.angle != prev_section.angle:
        #    result += self.create_turn_description(prev_section.angle)
        if self.ground_type != "" and (prev_section is None or prev_section.ground_type != self.ground_type):
            result += self.create_ground_type_description() + "\n"
        if self.slope != 0 and (prev_section is None or prev_section.slope != self.slope):
            result += self.create_slope_description() + "\n"
        if self.is_steps:
            result += self.create_steps_description() + "\n"
        if self.r_side_description != "" and (
                prev_section is None or prev_section.r_side_description != self.r_side_description):
            result += self.create_r_side_description() + "\n"
        if self.l_side_description != "" and (
                prev_section is None or prev_section.l_side_description != self.l_side_description):
            result += self.create_l_side_description() + "\n"
        if prev_section is None or prev_section.length != self.length:
            result += self.create_length_description() + "\n"
        if self.block != "" and (prev_section is None or prev_section.block != self.block):
            result += self.create_length_description() + "\n"
        if self.comments != "" and (prev_section is None or prev_section.comments != self.comments):
            result += self.create_comments_description() + "\n"
        if self.name != "" and (prev_section is None or prev_section.name != self.name):
            result += self.create_name_description() + "\n"
        return result
