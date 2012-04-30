from entity import Entity
from etypes import *
from fauna_actions import *

class Fauna(Entity):

    def __init__(self, name, walkable, action, reaction=idle()):
        super().__init__(name, walkable, FAUNA)
        self.action = action
        self.reaction = reaction

    def update(self, nomad, plains):
        self.action(self, nomad, plains)


def yak():
    return Fauna('yak', False, shuffle())
