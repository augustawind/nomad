import math
from collections import namedtuple

DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)

Point = namedtuple('Point', 'x y')

def points_in_circle(radius):
    for y in range(-radius, radius):
        for x in range(-radius, radius):
            if distance(0, 0, x, y) < radius:
                yield Point(x, y)


def distance(x, y, x2, y2):
    return math.sqrt(((x2 - x) ** 2) + ((y2 - y) ** 2))
