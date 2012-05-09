'''things that exist in the plains'''
from collections import OrderedDict, namedtuple

from nomad.util import DIRECTIONS

class Stats:

    def __init__(self, strength, agility, intelligence):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence


class Entity:
    '''A thing that exists in the plains.'''

    def __init__(self, name, walkable,
                 stats=Stats(strength=1.0, agility=1.0, intelligence=1.0),
                 as_matter=None, as_food=None, as_tool=None, as_actor=None,
                 as_reactor=None, as_mortal=None, as_tactile=None):
        self.name = name
        self.walkable = walkable
        self.stats = stats

        for attr in ('as_matter', 'as_food', 'as_tool', 'as_actor',
                     'as_reactor', 'as_mortal', 'as_tactile'):
            role = eval(attr)
            setattr(self, attr, role)
            if role:
                role.assign(self)

        self.x = None
        self.y = None
        self.plains = None

    def __str__(self):
        '''Return the entity's name.'''
        return self.name

    def _get_pos(self):
        return self.x, self.y
    def _set_pos(self, pos):
        self.x, self.y = pos
    pos = property(_get_pos, _set_pos, doc=
        '''Swizzle for (x, y).''')

    def get_accessable(self):
        '''Get all entities that are within this one's abilities to
        have access to.

        By default, this does the same thing as `get_in_reach`.
        This method can be overrided by subclasses to provide
        extended behavior.
        '''
        return self.get_in_reach()
    
    def get_in_reach(self):
        '''Return all entities within reach as a mapping of z coords
        to the entity underfoot and any unwalkable adjacent entities.
        '''
        z, entity = self.get_underfoot()
        in_reach = OrderedDict([(z, entity)])
        for dx, dy in DIRECTIONS:
            z, entity = self.get_adjacent(dx, dy)
            if entity.walkable:
                continue
            in_reach[z] = entity
        return in_reach 

    def get_underfoot(self):
        '''Return the z coordinate and the entity just under this one.'''
        return self.get_adjacent(0, 0, -1)

    def get_adjacent(self, dx, dy, dz=None):
        '''Return the z coordinate and entity adjacent to this one in the
        specified x, y, and z directions.
        '''
        if dz is None:
            z = -1
        else:
            z = self.plains.get_z(self) + dz
        return z, self.plains.get_entity(self.x + dx, self.y + dy, z)

    def update(self, nomad):
        '''Update the entity for each of its roles, given a `Nomad`.
        
        A `Role` may provide behavior for this method by overriding
        `Role.update`.
        '''
        for role in (getattr(self, a) for a in
                     ('as_matter', 'as_food', 'as_tool', 'as_actor',
                      'as_reactor', 'as_mortal', 'as_tactile')):
            if role:
                role.update(nomad)

    def put_underfoot(self, entity):
        '''Place an entity just under this one.'''
        if not entity:
            return
        z = self.plains.get_z(self)
        self.plains.add_entity(entity, self.x, self.y, z)
    
    def wait(self):
        '''Do nothing.'''
        pass

    def move(self, dx, dy):
        '''Move the entity in the given direction.'''
        assert None not in (self.x, self.y, self.plains)
        x = self.x + dx
        y = self.y + dy
        if not self.plains.walkable_at(x, y):
            return
        self.plains.move_fromto(self.x, self.y, x, y) 
