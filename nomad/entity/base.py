from collections import namedtuple

from nomad.entity.etypes import *

FoodData = namedtuple('FoodData', 'satiation nutrition')

defaultFood = FoodData(15, 0)

class Entity:
    '''A thing that exists in the plains.'''

    def __init__(self, name, walkable, etype='entity', as_food=None):
        self.name = name
        self.walkable = walkable
        self.etype = etype
        self.as_food = as_food

        self.x = None
        self.y = None
        self.plains = None

    def __str__(self):
        return self.name

    def update(self, nomad):
        '''Move the entity a step forward in time. Does nothing, but
        subclasses can override this method to provide behavior.
        '''
        pass

    def get_underfoot(self):
        '''Return the z coordinate and the entity just below the nomad.'''
        z = self.plains.get_z(self, self.x, self.y) - 1
        return z, self.plains.get_entity(self.x, self.y, z)
    
    def wait(self):
        pass

    def move(self, dx, dy):
        '''Move the entity in the given direction on its plains.'''
        assert None not in (self.x, self.y, self.plains)
        x = self.x + dx
        y = self.y + dy
        if not self.plains.walkable_at(x, y):
            return
        self.plains.move_fromto(self.x, self.y, x, y) 
