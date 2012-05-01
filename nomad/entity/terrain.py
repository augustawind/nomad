from nomad.entity.base import Entity
from nomad.entity.etypes import TERRAIN

class Terrain(Entity):

    def __init__(self, name, walkable, as_food=None):
        super().__init__(name, walkable, TERRAIN, as_food)

def earth(): return Terrain('earth', True)
def rock(): return Terrain('rock', False)

