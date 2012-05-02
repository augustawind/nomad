from nomad.entity.base import Entity
from nomad.entity.etypes import TOOL

class Tool(Entity):

    def __init__(self, name, walkable):
        super().__init__(name, walkable, TOOL)

def stick():
    return Tool('stick', True)

def sharp_rock():
    return Tool('sharp rock', True)

def spear():
    return Tool('spear', True)
