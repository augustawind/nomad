from random import randint

from nomad.util import *

def idle():
    def action(actor, nomad):
        pass
    return action


def shuffle():
    dirs = (DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN)
    def action(actor, nomad):
        i = randint(0, 3)
        dxy = dirs[i]
        actor.move(*dxy)
    return action


