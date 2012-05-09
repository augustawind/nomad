'''the dynamically generated world in which Nomad takes place'''
from nomad.entity import Entity
from nomad.util import *

class Plains:
    '''A shifting world that generates itself as it moves.'''

    def __init__(self, entities, floor_entity, generate):
        self.entities = entities
        self.floor_entity = floor_entity
        self.generate = generate

        self._init_entities(self.entities)

    @classmethod
    def with_floor(cls, floor_entity, generate, *shape_args, **shape_kws):
        shape_kws['default'] = lambda: [floor_entity()] 
        return cls(Octagon(*shape_args, **shape_kws),
                   floor_entity, generate)

    @staticmethod
    def _iter_entities(entities):
        for (x, y), ents in entities.items():
            for z, e in enumerate(ents):
                yield (x, y, z), e

    def _inform_entity(self, entity, x, y, z):
        '''Inform an entity of its xy positon.'''
        assert self.entities.in_bounds(x, y)
        entity.x = x
        entity.y = y 
        entity.z = z

    def _inform_entities(self, entities):
        '''Inform many  entities of their xy positions.'''
        for point, entity in self._iter_entities(entities):
            self._inform_entity(entity, *point)

    def _init_entity(self, entity, x, y, z):
        entity.plains = self
        self._inform_entity(entity, x, y, z)

    def _init_entities(self, entities):
        for (x, y, z), e in self._iter_entities(entities):
            self._init_entity(e, x, y, z)

    def walkable_at(self, x, y):
        '''Are all entities walkable at point (x, y)?'''
        xy = (x, y)
        return (xy in self.entities and
                all(e.walkable for e in self.entities[xy]))

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

    def z_in_bounds(self, x, y, z):
        '''Does an entity exist at (x, y, z)?'''
        return 0 <= z < len(self.entities[(x, y)])
    
    def add_entity(self, entity, x, y, z=-1):
        '''Add an entity at the given x, y, z. If z is -1, append it to
        the top.
        '''
        entities = self.entities[(x, y)]

        # If z is -1, append entity to the top.
        if z == -1:
            entities.append(entity)
            z = len(entities) - 1
        # Else, if z is in bounds, insert entity at z.
        elif self.z_in_bounds(x, y, z):
            entities.insert(z, entity)
            # Update z coords of above entities.
            for entity in entities[z:]:
                entity.z += 1
        # Otherwise, terminate.
        else:
            return
        # Initialize the entity at its new position.
        self._init_entity(entity, x, y, z)

    def pop_entity(self, x, y, z=-1):
        '''Remove and return the entity at the given x, y, z. If z is -1,
        pop the topmost entity.
        '''
        return self.entities[(x, y)].pop(z)

    def remove_entity(self, entity):
        entities = self.entities[entity.pos]
        z = entity.z
        # Delete the entity at its x, y, z position.
        del entities[z]
        # Update z coords of above entities.
        for entity in entities[z:]:
            entity.z -= 1

    def move_entity(self, entity, x, y, z=-1):
        '''Remove the entity at (x1, y1, z1) and add it to (x2, y2, z2).'''
        self.remove_entity(entity)
        self.add_entity(entity, x, y, z)

    def shift(self, dx, dy):
        assert dx or dy
        gen_coords = set()

        # Shift all entities by (dx, dy).
        entities = Octagon(*self.entities.params)
        for (x, y), ents in self.entities.items():
            new_point = Point(x + dx, y + dy)
            # Only move entity if new point is in bounds.
            if self.entities.in_bounds(*new_point):
                entities[new_point] = ents
            else:
                gen_coords.add(Point(-x, -y))

        # Generate new entities to fill open edge.
        new_entities = self.generate(self, gen_coords)
        self._init_entities(new_entities)
        self._inform_entities(entities)
        entities.update(new_entities)
        self.entities = entities


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

    def __init__(self, up, right, down, left, ul, ur, lr, ll,
                 default=lambda: None):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.ul = ul
        self.ur = ur 
        self.lr = lr
        self.ll = ll
        self.default = default

        self.params = (up, right, down, left, ul, ur, lr, ll, default)

        for y in range(self.up, self.down + 1):
            for x in range(self.left, self.right + 1):
                if self.in_bounds(x, y):
                    self[Point(x, y)] = default()

    def in_bounds(self, x, y):
        if x < self.left:  return False
        if x > self.right: return False
        if y < self.up:    return False
        if y > self.down:  return False

        if x - self.ul.x < self.ul.y - y: return False
        if x - self.ur.x < y - self.ur.y: return False
        if x - self.ll.x > y - self.ll.y: return False
        if x - self.lr.x > self.lr.y - y: return False

        return True


