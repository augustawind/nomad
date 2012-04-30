from entity import *

class Terrain(Entity):

    def __init__(self, name, walkable, as_food=None):
        super().__init__(name, walkable, 'terrain', as_food)

def earth(): return Terrain('earth', True)
def rock(): return Terrain('rock', False)

