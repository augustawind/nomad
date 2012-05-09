'''things that exist in the plains'''
from collections import OrderedDict, namedtuple
from itertools import chain

from nomad.util import DIRECTIONS

class Stats:

    def __init__(self, strength, agility, intelligence):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence


class Entity:
    '''A thing that exists in the plains.'''

    def __init__(self, name, walkable, moveable=True,
                 stats=Stats(strength=1.0, agility=1.0, intelligence=1.0),
                 roles={}):
        self.name = name
        self.walkable = walkable
        self.moveable = moveable
        self.stats = stats

        self.roles = roles
        for role in self.roles.values():
            role.assign(self)

        self.held_entities = []

        self.x = None
        self.y = None
        self.z = None
        self.plains = None

    def __str__(self):
        '''Return the entity's name.'''
        return self.name

    def get_role(self, role_name):
        return self.roles.get(role_name, None)

    as_matter = property(lambda self: self.get_role('matter'))
    as_edible = property(lambda self: self.get_role('edible'))
    as_usable = property(lambda self: self.get_role('usable'))
    as_actor = property(lambda self: self.get_role('actor'))
    as_reactor = property(lambda self: self.get_role('reactor'))
    as_mortal = property(lambda self: self.get_role('mortal'))
    as_tactile = property(lambda self: self.get_role('tactile'))

    def _get_pos(self):
        return self.x, self.y
    def _set_pos(self, pos):
        self.x, self.y = pos
    pos = property(_get_pos, _set_pos, doc=
        '''Swizzle for (x, y).''')
    
    def get_in_reach(self):
        in_reach = []
        for entity in chain(self.held_entities, [self.get_underfoot()]):
            in_reach.append(entity)
        neighbors = (self.get_adjacent(dx, dy) for dx, dy in DIRECTIONS)
        for entity in neighbors:
            if not entity.walkable:
                in_reach.append(entity)
        return in_reach 

    def get_underfoot(self):
        '''Return the entity just under this one.'''
        return self.get_adjacent(0, 0, -1)

    def get_adjacent(self, dx, dy, dz=None):
        '''Return the entity adjacent to this one in the given x, y, and z
        directions.
        '''
        if dz is None:
            z = -1
        else:
            z = self.z + dz
        return self.plains.get_entity(self.x + dx, self.y + dy, z)

    def update(self, nomad):
        '''Update the entity for each of its roles, given a `Nomad`.
        
        A `Role` may provide behavior for this method by overriding
        `Role.update`.
        '''
        for role in self.roles.values():
            if role:
                role.update(nomad)

    def put_underfoot(self, entity):
        '''Place an entity just under this one.'''
        if not entity:
            return
        self.plains.add_entity(entity, self.x, self.y, self.z)

    def damage(self, dmg):
        damaged = False
        for role in self.roles.values():
            if role:
                damaged = role.damage(dmg) or damaged
    
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
        self.plains.move_entity(self, x, y) 
