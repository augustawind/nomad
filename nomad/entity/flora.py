from nomad.entity.base import Entity, FoodData, defaultFood
from nomad.entity.etypes import FLORA
from nomad.entity.role import *

class Flora(Entity):

    def __init__(self, name, walkable, as_food):
        super().__init__(name, walkable, FLORA, as_food)


def grass(): return Flora('grass', True, Edible(0, -5))
def flower(): return Flora('flower', True, Edible(0, -1)) 
def mushroom(): return Flora('mushroom', True, Edible(10, 1))
