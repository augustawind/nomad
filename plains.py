from collections import namedtuple
import math

import plainsgen

Point = namedtuple('Point', 'x y')

class Plains:

    def __init__(self, radius, entities, gen_strategy=None):
        self.radius = radius
        self.entities = entities
        self.gen_strategy = gen_strategy

    @classmethod
    def with_bg(cls, radius, bg_entity):
        entities = {}
        for point in points_in_circle(radius):
            entities[point] = [bg_entity]
        
        return cls(radius, entities,
                   gen_strategy=plainsgen.background(bg_entity))

    def get_entity(self, x, y, z=-1):
        return self.entities[(x, y)][z]
    
    def add_entity(self, entity, x, y, z=-1):
        xy = (x, y)
        if xy in self.entities:
            entities = self.entities[xy]
            if z < 0 or z >= len(entities):
                entities.append(entity)
            else:
                entities.insert(z, entity)
        elif distance(0, 0, x, y) <= self.radius:
            self.entities[xy] = [entity]

    def shift(self, dx, dy):
        pass


def points_in_circle(radius):
    for y in range(-radius, radius):
        for x in range(-radius, radius):
            if distance(0, 0, x, y) < radius:
                yield Point(x, y)

def distance(x, y, x2, y2):
    return math.sqrt(((x2 - x) ** 2) + ((y2 - y) ** 2))
