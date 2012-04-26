from curses import *
from functools import partial

import flora
from nomad import *
from plains import *

VIEW_WIDTH = 18
VIEW_HEIGHT = 18

command = {
    KEY_LEFT:  partial(move_nomad, 0, -1),
    KEY_RIGHT: partial(move_nomad, 0, 1),
    KEY_UP:    partial(move_nomad, -1, 0),
    KEY_DOWN:  partial(move_nomad, 1, 0)
    }

ent2chr = {
    'nomad': '@',
    'grass': '"',
    }

def main(stdscr): 
    nomad = Nomad()
    plains = Plains.with_bg(nomad.los, flora.grass)
    plains.add_entity(nomad, 0, 0)

    plains_win = newwin(VIEW_HEIGHT, VIEW_WIDTH, 0, 0) 

    while True:
        update(plains_win, nomad, plains)
        stdscr.refresh()

        key = stdscr.getch()
        if key in command:
            command[key](nomad, plains)


'''
def get_player_name(win):
    win.addstr("What is your name? ")
    return win.getstr()
'''


def update(win, nomad, plains):
    win.clear()

    radius = nomad.los
    coords = range(-radius, radius + 1)
    for y in coords:
        for x in coords:
            distance = math.sqrt((x ** 2) + (y ** 2))
            if distance < radius:
                entity = plains.get_entity(x, y)
                char = ent2chr[entity.name]
            else:
                char = ' '
            win.addnstr(y + radius, x + radius, char, 1)

    win.refresh()


if __name__ == '__main__':
    stdscr = initscr()
    wrapper(main)

