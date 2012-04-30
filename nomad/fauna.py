from nomad.entity import Entity
from nomad.etypes import *
from nomad.fauna_actions import *

MIN_SATIATION = 0
MAX_SATIATION = 100
MIN_HEALTH = 0
MAX_HEALTH = 100

LOW_HEALTH_LINE = (MAX_HEALTH - MIN_HEALTH) // 2

SATIATION_DECAY = 0.25
HEALTH_DECAY = 0.025

class Fauna(Entity):

    def __init__(self, name, walkable, action, reaction=idle(),
                 satiation=MAX_SATIATION, health=MAX_HEALTH):
        super().__init__(name, walkable, FAUNA)
        self.action = action
        self.reaction = reaction
        self.satiation = satiation
        self.health = health

    def update(self, nomad):
        self.action(self, nomad)
        self.satiation -= SATIATION_DECAY
        self.health -= HEALTH_DECAY 

        if self.health < LOW_HEALTH_LINE:
            self.handle_low_health()

    @property
    def alive(self):
        return self.satiation > 0

    def _get_satiation(self):
        return self._satiation
    def _set_satiation(self, x):
        self._satiation = max(MIN_SATIATION, min(MAX_SATIATION, x))
    satiation = property(_get_satiation, _set_satiation)

    def _get_health(self):
        return self._health
    def _set_health(self, x):
        self._health = max(MIN_HEALTH, min(MAX_HEALTH, x))
    health = property(_get_health, _set_health)

    def handle_low_health(self):
        self.satiation -= (LOW_HEALTH_LINE - self.health)

    def eat(self, entity):
        '''Attempt to eat an entity. Return True if successful, else False.'''
        food = entity.as_food
        if food:
            self.satiation = self.satiation + food.satiation
            self.health = self.health + food.nutrition
            return True
        return False

    def eat_underfoot(self):
        '''Attempt to eat the entity underfoot.'''
        z, entity = self.get_underfoot()
        if self.eat(entity):
            self.plains.pop_entity(self.x, self.y, z)


def yak():
    return Fauna('yak', False, shuffle())
