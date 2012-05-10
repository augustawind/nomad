import math
from collections import namedtuple

DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)
DIR_UPLEFT = (-1, -1)
DIR_UPRIGHT = (1, -1)
DIR_DOWNLEFT = (-1, 1)
DIR_DOWNRIGHT = (1, 1)
DIRECTIONS = (DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT,
              DIR_UPLEFT, DIR_UPRIGHT, DIR_DOWNLEFT, DIR_DOWNRIGHT)

Point = namedtuple('Point', 'x y')

def edge_coord(origin, radius, trig_func, degrees):
    return origin + radius * trig_func(degrees * math.pi / 180) 

def edge_point(origin_x, origin_y, radius, degrees):
    return (edge_coord(origin_x, radius, math.cos, degrees),
            edge_coord(origin_y, radius, math.sin, degrees))


def points_in_circle(radius):
    for y in range(-radius, radius):
        for x in range(-radius, radius):
            if distance(0, 0, x, y) < radius:
                yield Point(x, y)


def points_in_octagon(side):
    points = set()
    size = side * 3
    half_size = size // 2
    half_side = side // 2
    for y in range(-half_size - 1, half_size + 1):
        x1 = -half_side - (side - abs(y))
        x2 = half_side + (side - abs(y)) + 1
        for x in range(x1, x2):
            points.add((x, y))
    return points


def distance(x, y, x2, y2):
    return math.sqrt(((x2 - x) ** 2) + ((y2 - y) ** 2))

def flatten_keys(d):
    return dict((key, v) for keys, v in d.items() for key in keys)
