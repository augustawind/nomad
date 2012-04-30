from random import randint

DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)

def idle():
    def action(actor, nomad, plains):
        pass
    return action

def shuffle():
    dirs = (DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN)
    def action(actor, nomad, plains):
        i = randint(0, 3)
        dxy = dirs[i]
        actor.move(plains, *dxy)
    return action


