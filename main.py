from curses import *
from functools import partial

import flora
import terrain
import generators as gen
from nomad import *
from plains import *

VIEW_WIDTH = 78
VIEW_HEIGHT = 23

PAIR_RED = 1
PAIR_GREEN = 2
PAIR_YELLOW = 3
PAIR_BLUE = 4
PAIR_MAGENTA = 5
PAIR_CYAN = 6
PAIR_WHITE = 7

command = {
    KEY_LEFT:  partial(move_nomad, -1, 0),
    KEY_RIGHT: partial(move_nomad, 1, 0),
    KEY_UP:    partial(move_nomad, 0, -1),
    KEY_DOWN:  partial(move_nomad, 0, 1),
    }

ent_display = {
    'nomad': ('@', PAIR_YELLOW),
    'grass': ('"', PAIR_GREEN),
    'flower': ('*', PAIR_WHITE),
    'earth': ('.', PAIR_WHITE),
    'rock': ('0', PAIR_CYAN),
    }

def main(stdscr): 
    init_pair(PAIR_RED, COLOR_RED, -1)
    init_pair(PAIR_GREEN, COLOR_GREEN, -1)
    init_pair(PAIR_YELLOW, COLOR_YELLOW, -1)
    init_pair(PAIR_BLUE, COLOR_BLUE, -1)
    init_pair(PAIR_MAGENTA, COLOR_MAGENTA, -1)
    init_pair(PAIR_CYAN, COLOR_CYAN, -1)
    init_pair(PAIR_WHITE, COLOR_WHITE, -1)

    nomad = Nomad(los=9)
    plains = Plains.with_floor(nomad.los, terrain.earth,
                               gen.chance({90: flora.grass, 10: flora.flower,
                                           1: terrain.rock}))
    plains.add_entity(nomad, 0, 0)

    plains_win = newwin(VIEW_HEIGHT, VIEW_WIDTH, 0, 0) 

    while True:
        update(plains_win, nomad, plains)
        stdscr.refresh()

        key = stdscr.getch()
        if key in command:
            command[key](nomad, plains)


def update(win, nomad, plains):
    win.clear()

    radius = nomad.los
    coords = range(-radius, radius + 1)
    for y in coords:
        for x in coords:
            if (x, y) in plains.entities:
                entity = plains.get_entity(x, y)
                char, color = ent_display[entity.name]
            else:
                char = ' '
                color = PAIR_WHITE
            win.addnstr(y + radius, x + radius, char, 1, color_pair(color))

    win.refresh()

if __name__ == '__main__':
    stdscr = initscr()
    start_color()
    use_default_colors()
    curs_set(0)

    wrapper(main)

    curs_set(1)
