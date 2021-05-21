from django import forms
import svgpathtools
from xml.dom import minidom
import cmath
import numpy as np


def get_polars(z):
    r, theta = cmath.polar(z)
    return (r, np.degrees(theta))


def get_path_coordinates(path):
    d_string = path.attributes['d'].value
    start, end = svgpathtools.parse_path(d_string)[0]
    return [get_polars(start), get_polars(end)]


class SVGImageParseService:
    image = forms.FileField

    @classmethod
    def call(cls, file):
        file = minidom.parse(file)
        paths = file.getElementsByTagName("path")
        list = []
        for path in paths:
            list.append(get_path_coordinates(path))
        return list
