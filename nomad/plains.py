'''the dynamically generated world in which Nomad takes place'''
from nomad.entity import Entity
from nomad.util import *

class Octagon(dict):
    '''A mapping of (x, y) tuples to arbitrary values. The coordinates
    form an octagon.

    `Properties`
        `up` : int
            Lower y boundary.
        `down` : int
            Upper y boundary.
        `left` : int
            Lower x boundary.
        `right` : int
            Upper x boundary.
        `ul` : `Point`
            Upper Left diagonal boundary.
        `ur` : `Point`
            Upper Right diagonal boundary.
        `lr` : `Point`
            Lower Right diagonal boundary.
        `ll` : `Point`
            Lower Left diagonal boundary.
    '''

    def __init__(self, up, right, down, left, ul, ur, lr, ll, default=None):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.ul = ul
        self.ur = ur 
        self.lr = lr
        self.ll = ll

        for y in range(self.up, self.down + 1):
            for x in range(self.left, self.right + 1):
                if self.in_bounds(x, y):
                    self[(x, y)] = default

    def in_bounds(self, x, y):
        if x < self.left:  return False
        if x > self.right + 1: return False
        if y < self.up:    return False
        if y > self.down + 1:  return False

        if x - self.ul.x < self.ul.y - y: return False
        if x - self.ur.x < y - self.ur.y: return False
        if x - self.ll.x > y - self.ll.y: return False
        if x - self.lr.x > self.lr.y - y: return False

        return True


class Plains:
    '''A shifting world that generates itself as it moves.'''

    def __init__(self, entities, floor_entity, generate):
        self.entities = entities
        self.floor_entity = floor_entity
        self.generate = generate

        self._init_entities(self.entities)

    @classmethod
    def with_floor(cls, floor_entity, generate, *shape_args, **shape_kws):
        shape_kws['default'] = [floor_entity] 
        return cls(Octagon(*shape_args, **shape_kws),
                   floor_entity, generate)

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

    def get_z(self, entity):
        '''Return the z coordinate of an entity on this plains.'''
        x, y = entity.pos
        return self.entities[(x, y)].index(entity)

    def get_entity(self, x, y, z=-1):
        '''Return the entity at the given coordinates on this plains.'''
        return self.entities[(x, y)][z]

    def get_entities(self):
        '''Yield each entity on this plains in an arbitrary order.'''
        for ents in self.entities.values():
            for ent in ents:
                yield ent

    def get_coords(self):
        '''Yield an x, y, z triplet for each coordinate on this plains.'''
        for (x, y), ents in self.entities.items():
            for z in range(len(ents)):
                yield x, y, z
    
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
        elif self.entities.in_bounds(x, y):
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
        assert dx or dy

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

        if dx:
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

    def shift(self, dx, dy):
        '''Shift the plains in the given x and y directions.'''
        assert dx or dy

        gen_coords = []
        del_coords = []

        def update_coords(d, to_gen, to_del):
            if d < 0:
                gen_coords.append(to_gen)
                del_coords.append(to_del)
            else:
                del_coords.append(to_gen)
                gen_coords.append(to_del)

        for x, y in self.entities:
            xs = []
            ys = []
            for x_, y_ in self.entities:
                if y_ == y: xs.append(x_)
                if x_ == x: ys.append(y_)

            dy_gen = (x, min(ys))
            dy_del = (x, max(ys))
            dx_gen = (min(xs), y)
            dx_del = (max(xs), y)
            if dy and not dx:
                update_coords(dy, dy_gen, dy_del)
            elif dx and not dy:
                update_coords(dx, dx_gen, dy_del)
            elif dx and dy:
                to_gen = (dy_gen + dx_gen) // 2
                to_del = (dy_del + dx_del) // 2
                update_coords = (dx * dy, to_gen, to_del)


        new_entities = {}
        for x, y in self.entities:
            p = (x, y)
            if p in del_coords:
                continue
            new_entities[(x - dx, y - dy)] = self.entities[p]

        edge_entities = self.generate(self, gen_coords)
        self._init_entities(edge_entities)
        self._inform_entities(new_entities)
        new_entities.update(edge_entities)
        self.entities = new_entities
