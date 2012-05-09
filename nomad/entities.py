'''entity definitions'''
import random

from nomad.entity import Entity
from nomad.roles import *
from nomad.util import DIRECTIONS

def shuffle(actor, nomad):
    dx, dy = random.choice(DIRECTIONS)
    actor.move(dx, dy)

def strike(tool, actor, target):
    target.damage(tool.as_matter.weight)


def earth(): return Entity(
    'earth', True, False)
def rock(): return Entity(
    'rock', False)

def grass(): return Entity(
    'grass', True, roles={
        'edible': Edible(0, -5)})
def flower(): return Entity(
    'flower', True, roles={
        'edible': Edible(0, -1)}) 
def mushroom(): return Entity(
    'mushroom', True, roles={
        'edible': Edible(10, 1)})

def stick(): return Entity(
    'stick', True, roles={
        'matter': Matter(25, 25),
        'usable': Usable(strike)})
def sharp_rock(): return Entity(
    'sharp rock', True, roles={
        'matter': Matter(25, 25),
        'usable': Usable(strike)})
def spear(): return Entity(
    'spear', True, roles={
        'matter': Matter(25, 25),
        'usable': Usable(strike)})

def yak(): return Entity(
    'yak', False, roles={
        'actor': Actor(shuffle)})
