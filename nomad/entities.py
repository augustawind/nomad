import random

from nomad.entity import Entity
from nomad.roles import *
from nomad.util import DIRECTIONS

def shuffle(actor, nomad):
    dx, dy = random.choice(DIRECTIONS)
    actor.move(dx, dy)

def strike(tool, actor, target):
    target.damage(tool.as_matter.weight)

def earth(): return Entity('earth', True)
def rock(): return Entity('rock', False)

def grass(): return Entity('grass', True, as_food=Edible(0, -5))
def flower(): return Entity('flower', True, as_food=Edible(0, -1)) 
def mushroom(): return Entity('mushroom', True, as_food=Edible(10, 1))

def stick(): return Entity('stick', True, as_matter=Matter(25, 25),
                                          as_tool=Tool(strike))
def sharp_rock(): return Entity('sharp rock', True, as_matter=Matter(25, 25),
                                                    as_tool=Tool(strike))
def spear(): return Entity('spear', True, as_matter=Matter(25, 25),
                                          as_tool=Tool(strike))

def yak(): return Entity('yak', False, as_actor=Actor(shuffle))
