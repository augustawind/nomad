from nomad.entity import Entity
from nomad.roles import *
from nomad.entities import *


class Nomad(Entity):

    tool_factory = {
        frozenset(('sharp rock', 'stick')): spear
        }

    def __init__(self, los=5):
        super().__init__('nomad', False,
                         as_mortal=Mortal(),
                         as_tactile=Tactile(self.tool_factory))
        self.los = los

    def move(self, dx, dy):
        if not self.plains.walkable_at(self.x + dx, self.y + dy):
            return
        self.plains.shift(dx, dy)
        self.plains.move_fromto(self.x, self.y, self.x + dx, self.y + dy)
