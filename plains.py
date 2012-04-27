from util import *

class Plains:

    def __init__(self, radius, entities, floor_entity, generate=None):
        self.radius = radius
        self.entities = entities
        self.floor_entity = floor_entity
        self.generate = generate

    @classmethod
    def with_floor(cls, radius, floor_entity, generate=None):
        entities = {}
        for point in points_in_circle(radius):
            entities[point] = [floor_entity]
        
        return cls(radius, entities, floor_entity, generate=generate)

    def walkable_at(self, x, y):
        return all(entity.walkable for entity in self.entities[(x, y)])

    def get_entity(self, x, y, z=-1):
        return self.entities[(x, y)][z]

    def get_coords(self):
        return self.entities.keys()
    
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

    def pop_entity(self, x, y, z=-1):
        xy = (x, y)
        if xy in self.entities:
            if z < 0 or z >= len(self.entities[xy]):
                return self.entities[xy].pop()
            else:
                return self.entities[xy].pop(z)

    def move_fromto(self, x1, y1, x2, y2, z1=-1, z2=-1):
        entity = self.pop_entity(x1, y1, z1)
        self.add_entity(entity, x2, y2, z2)

    def shift(self, dx, dy):
        if not (dx or dy) or (dx and dy):
            return

        gen_coords = []
        del_coords = []
        if dy:
            xs = set(x for x, y in self.entities)
            for x in xs:
                y1 = min(y for x_, y in self.entities if x_ == x)
                y2 = max(y for x_, y in self.entities if x_ == x)
                p1 = (x, y1)
                p2 = (x, y2)
                if dy < 0:
                    gen_coords.append(p1)
                    del_coords.append(p2)
                else:
                    del_coords.append(p1)
                    gen_coords.append(p2)
                    
            edge_coords = gen_coords if dx < 0 else del_coords
        elif dx:
            ys = set(y for x, y in self.entities)
            for y in ys:
                x1 = min(x for x, y_ in self.entities if y_ == y)
                x2 = max(x for x, y_ in self.entities if y_ == y)
                p1 = (x1, y)
                p2 = (x2, y)
                if dx < 0:
                    gen_coords.append(p1)
                    del_coords.append(p2)
                else:
                    del_coords.append(p1)
                    gen_coords.append(p2)

        new_entities = {}
        for x, y in self.entities:
            p = (x, y)
            if p in del_coords:
                continue
            new_entities[(x - dx , y - dy)] = self.entities[p]

        edge_entities = self.generate(self, gen_coords)
        new_entities.update(edge_entities)
        self.entities = new_entities
