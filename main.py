from curses import *
from functools import partial

import fauna
import flora
import terrain
import strategy.plainsgen as gen
from fauna_actions import DIR_LEFT, DIR_RIGHT, DIR_UP, DIR_DOWN
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

KEY = ord

command = {
    KEY('h'): partial(move_nomad, *DIR_LEFT),
    KEY('l'): partial(move_nomad, *DIR_RIGHT),
    KEY('k'): partial(move_nomad, *DIR_UP),
    KEY('j'): partial(move_nomad, *DIR_DOWN),
    KEY('s'): lambda n, p: None,
    }

ent_display = {
    'nomad': ('@', PAIR_YELLOW),
    'grass': ('"', PAIR_GREEN),
    'flower': ('*', PAIR_WHITE),
    'earth': ('.', PAIR_WHITE),
    'rock': ('0', PAIR_CYAN),
    'yak': ('Y', PAIR_RED),
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
    plains = Plains.with_floor(nomad.los, terrain.earth, gen.chance(
                               {90: flora.grass, 10: flora.flower,
                                2: terrain.rock, 1: fauna.yak}))
    plains.add_entity(nomad, 0, 0)

    plains_win = newwin(VIEW_HEIGHT, VIEW_WIDTH, 0, 0) 

    while True:
        refresh(plains_win, nomad, plains)
        stdscr.refresh()

        key = stdscr.getch()
        if key in command:
            command[key](nomad, plains)

        update_fauna(nomad, plains)

def refresh(win, nomad, plains):
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


def update_fauna(nomad, plains):
    for entity in tuple(plains.get_fauna()):
        entity.update(nomad, plains)

if __name__ == '__main__':
    stdscr = initscr()
    start_color()
    use_default_colors()
    curs_set(0)

    wrapper(main)

    curs_set(1)
