from collections import namedtuple

from etypes import *

MAX_SATIATION = 100
MAX_NUTRITION = 100

FoodData = namedtuple('FoodData', 'edible satiation nutrition')

defaultFood = FoodData(True, 35, 15)

class Entity:
    '''A thing that exists in the plains.'''

    def __init__(self, name, walkable, etype='entity', satiation=MAX_SATIATION,
                 nutrition=MAX_NUTRITION, as_food=None):
        self.name = name
        self.walkable = walkable
        self.etype = etype
        self.satiation = satiation
        self.nutrition = nutrition
        self.as_food = as_food

        self.x = None
        self.y = None
        self.plains = None

    def update(self, nomad):
        '''Move the entity a step forward in time. Does nothing, but
        subclasses can override this method to provide behavior.
        '''
        pass

    def get_underfoot(self):
        z = self.plains.get_z(self, self.x, self.y)
        return self.plains.get_entity(self.x, self.y, z - 1)

    def move(self, dx, dy):
        '''Move the entity in the given direction on its plains.'''
        assert None not in (self.x, self.y, self.plains)
        x = self.x + dx
        y = self.y + dy
        if not self.plains.walkable_at(x, y):
            return
        self.plains.move_fromto(self.x, self.y, x, y) 

    def eat(self, entity):
        '''Attempt to eat an entity. Return True if successful, else False.'''
        food = entity.as_food
        if food and food.edible:
            self.satiation = min(MAX_SATIATION, food.satiation)
            self.nutrition = min(MAX_NUTRITION, food.nutrition)
            return True
        return False

    def eat_underfoot(self):
        '''Attempt to eat the entity underfoot.'''
        entity = self.get_underfoot()
        if self.eat(entity):
            self.plains.pop_entity(self.x, self.y,
                                   self.plains.get_z(entity, self.x, self.y))
