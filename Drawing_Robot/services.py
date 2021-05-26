from xml.dom import minidom
from math import atan2, degrees, ceil, pi, sqrt
from svg.path import parse_path
from svg.path.path import Line
import json

LEFT_TURN = "Left"
RIGHT_TURN = "Right"


def find_angle(x1, y1, x2, y2):
    return degrees(atan2(y2 - y1, x2 - x1))


def angle_trunc(a):
    while a < 0.0:
        a += pi * 2
    return a


def get_angle_from_x_axis(x0, y0, x1, y1):
    delta_y = y0 - y1
    delta_x = x1 - x0
    return degrees(angle_trunc(atan2(delta_y, delta_x)))


def get_coordinates(path):
    coordinates = []
    prev_angle_btw_points = 0
    prev_angle_from_x_axis = 0
    for ind, val in enumerate(path):
        if isinstance(val, Line):
            x0 = ceil(val.start.real)
            y0 = ceil(val.start.imag)
            x1 = ceil(val.end.real)
            y1 = ceil(val.end.imag)
            edge = ceil(sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2))
            angle_btw_points = abs(ceil(find_angle(x0, y0, x1, y1)))
            angle_from_x_axis = ceil(get_angle_from_x_axis(x0, y0, x1, y1))
            if ind == 0:
                rotation_angle = angle_btw_points
                turn = LEFT_TURN
            else:
                rotation_angle = angle_btw_points - prev_angle_btw_points

                if angle_from_x_axis > prev_angle_from_x_axis:
                    turn = LEFT_TURN
                else:
                    turn = RIGHT_TURN

            prev_angle_btw_points = angle_btw_points
            prev_angle_from_x_axis = angle_from_x_axis

            coordinates.append({'edge': edge,
                                'angle': abs(rotation_angle),
                                'turn': turn})
    return coordinates


class SVGImageParseService:
    # image = forms.FileField
    @classmethod
    def call(cls, file):
        doc = minidom.parse(file)
        path_strings = [path.getAttribute('d') for path
                        in doc.getElementsByTagName('path')]
        doc.unlink()
        for path in path_strings:
            path = parse_path(path)
            coordinates = get_coordinates(path)
            json_object = json.dumps(coordinates)
        return json_object
