from entity import *

class Nomad(Entity):

    def __init__(self, los=6):
        super().__init__('nomad')
        self.los = los

def move_nomad(dx, dy, nomad, plains):
    plains.shift(dx, dy)
    plains.add_entity(nomad, 0, 0)
