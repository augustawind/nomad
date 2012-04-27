from entity import *

class Nomad(Entity):

    def __init__(self, los=6):
        super().__init__('nomad', False)
        self.los = los

def move_nomad(dx, dy, nomad, plains):
    if not plains.walkable_at(dx, dy):
        return
    plains.shift(dx, dy)
    plains.move_fromto(-dx, -dy, 0, 0)
