import curses
from functools import partial

import fauna
import flora
import terrain
import plainsgen as gen
from nomad import *
from plains import *
from util import *

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

def player_commands():
    return {
        KEY('h'): partial(move_nomad, *DIR_LEFT),
        KEY('l'): partial(move_nomad, *DIR_RIGHT),
        KEY('k'): partial(move_nomad, *DIR_UP),
        KEY('j'): partial(move_nomad, *DIR_DOWN),
        KEY('s'): lambda n: None,

        KEY('e'): Nomad.eat_underfoot,
        }


def render_info():
    return {
        'nomad': ('@', PAIR_YELLOW),
        'grass': ('"', PAIR_GREEN),
        'flower': ('*', PAIR_WHITE),
        'earth': ('.', PAIR_WHITE),
        'rock': ('0', PAIR_CYAN),
        'yak': ('Y', PAIR_RED),
        'mushroom' : ('?', PAIR_MAGENTA),
        }


def init_color_pairs():
    for (n, fg_color) in (
            (PAIR_RED, curses.COLOR_RED),
            (PAIR_GREEN, curses.COLOR_GREEN),
            (PAIR_YELLOW, curses.COLOR_YELLOW),
            (PAIR_BLUE, curses.COLOR_BLUE),
            (PAIR_MAGENTA, curses.COLOR_MAGENTA),
            (PAIR_CYAN, curses.COLOR_CYAN),
            (PAIR_WHITE, curses.COLOR_WHITE)):
        curses.init_pair(n, fg_color, -1)


def main(stdscr): 
    init_color_pairs()
    nomad = Nomad(los=9)
    plains = Plains.with_floor(nomad.los, terrain.earth, gen.chance(
                               {90: flora.grass, 10: flora.flower,
                                3: flora.mushroom,
                                2: terrain.rock, 1: fauna.yak}))
    plains.add_entity(nomad, 0, 0)

    plains_win = curses.newwin(VIEW_HEIGHT, VIEW_WIDTH, 0, 0) 

    display_dict = render_info()
    command_dict = player_commands()
    while True:
        refresh(plains_win, display_dict, nomad, plains)
        stdscr.refresh()

        key = stdscr.getch()
        if key in command_dict:
            command_dict[key](nomad)

        update_fauna(nomad, plains)


def refresh(win, display_dict, nomad, plains):
    win.clear()

    radius = nomad.los
    coords = range(-radius, radius + 1)
    for y in coords:
        for x in coords:
            if (x, y) in plains.entities:
                entity = plains.get_entity(x, y)
                char, color = display_dict[entity.name]
            else:
                char = ' '
                color = PAIR_WHITE
            win.addnstr(y + radius, x + radius, char, 1,
                        curses.color_pair(color))

    win.refresh()


def update_fauna(nomad, plains):
    for entity in tuple(plains.get_fauna()):
        entity.update(nomad)


if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)

    curses.wrapper(main)

    curses.curs_set(1)
