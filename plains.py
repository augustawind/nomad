from entity import *
from util import *

class Plains:
    '''A shifting world that generates itself as it moves.'''

    def __init__(self, radius, entities, floor_entity, generate=None):
        self.radius = radius
        self.entities = entities
        self.floor_entity = floor_entity
        self.generate = generate

        self._init_entities(self.entities)

    @classmethod
    def with_floor(cls, radius, floor_entity, generate=None):
        entities = {}
        for point in points_in_circle(radius):
            entities[point] = [floor_entity()]
        
        return cls(radius, entities, floor_entity, generate=generate)

    @staticmethod
    def _iter_entities(entities):
        for (x, y), ents in entities.items():
            for z, e in enumerate(ents):
                yield (x, y, z), e

    @staticmethod
    def _inform_entity(entity, x, y):
        '''Inform an entity of its xy positon.'''
        entity.x = x
        entity.y = y 

    @classmethod
    def _inform_entities(cls, entities):
        '''Inform many  entities of their xy positions.'''
        for (x, y, z), e in cls._iter_entities(entities):
            e.x = x
            e.y = y

    def _init_entity(self, entity, x, y):
        entity.plains = self
        self._inform_entity(entity, x, y)

    def _init_entities(self, entities):
        for (x, y, z), e in self._iter_entities(entities):
            self._init_entity(e, x, y)
    
    def in_bounds(self, x, y):
        '''Are the given x and y within the plains's borders?'''
        return distance(0, 0, x, y) <= self.radius

    def z_in_bounds(self, x, y, z):
        '''Does an entity exist at (x, y, z), given that at least one
        exists at x and y?
        '''
        return 0 <= z < len(self.entities[(x, y)])

    def walkable_at(self, x, y):
        '''Are all entities walkable at point (x, y)?'''
        xy = (x, y)
        return (xy in self.entities and
                all(e.walkable for e in self.entities[xy]))

    def get_z(self, entity, x, y):
        return self.entities[(x, y)].index(entity)

    def get_entity(self, x, y, z=-1):
        return self.entities[(x, y)][z]

    def get_coords(self):
        return self.entities.keys()
    
    def get_fauna(self):
        '''Return all entities with an etype of FAUNA.'''
        for entities in self.entities.values():
            for entity in entities:
                if entity.etype is FAUNA:
                    yield entity

    def add_entity(self, entity, x, y, z=-1):
        '''Add an entity at the given x, y, z. If z is out of bounds, append it
        to the top.
        '''
        xy = (x, y)
        if xy in self.entities:
            entities = self.entities[xy]
            if self.z_in_bounds(x, y, z):
                entities.insert(z, entity)
            else:
                entities.append(entity)
        elif self.in_bounds(x, y):
            self.entities[xy] = [entity]

        self._init_entity(entity, x, y)

    def pop_entity(self, x, y, z=-1):
        '''Remove and return the entity at the given x, y, z. If z is out of
        bounds, pop the topmost entity. If no entity exists there, return None.
        '''
        xy = (x, y)
        if xy in self.entities:
            ents = self.entities[xy]
            if z < 0 or z >= len(ents):
                entity = ents.pop()
            else:
                entity = ents.pop(z)
            if not ents:
                del self.entities[xy]
            return entity

    def move_fromto(self, x1, y1, x2, y2, z1=-1, z2=-1):
        '''Remove the entity at (x1, y1, z1) and add it to (x2, y2, z2).'''
        entity = self.pop_entity(x1, y1, z1)
        self.add_entity(entity, x2, y2, z2)

    def shift(self, dx, dy):
        '''Shift the plains in the given x and y directions.'''
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
        self._init_entities(edge_entities)
        self._inform_entities(new_entities)
        new_entities.update(edge_entities)
        self.entities = new_entities
