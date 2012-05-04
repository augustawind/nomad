import curses
from curses import *
from functools import partial

from nomad.entities import *
from nomad.nomad import Nomad
from nomad.plains import Plains, gen
from nomad.util import *

PLAINS_WIN = (20, 20, 0, 0)
STATUS_WIN = (20, 20, 0, 21)

PAIR_RED = 1
PAIR_GREEN = 2
PAIR_YELLOW = 3
PAIR_BLUE = 4
PAIR_MAGENTA = 5
PAIR_CYAN = 6
PAIR_WHITE = 7

KEY = ord

def run():
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    curses.wrapper(main)
    curses.curs_set(1)


def main(stdscr): 
    init_color_pairs()

    nomad = Nomad(los=9)
    plains = Plains.with_floor(nomad.los, earth, gen.chance(
                               {90: grass, 10: flower,
                                3: mushroom, 5: stick,
                                2: sharp_rock, 1: yak}))
    plains.add_entity(nomad, 0, 0)

    plains_win = curses.newwin(*PLAINS_WIN) 
    status_win = curses.newwin(*STATUS_WIN)

    display_dict = render_info()
    command_dict = player_commands()
    while nomad.as_mortal.alive:
        update_plains_window(plains_win, display_dict, nomad, plains)
        update_status_window(status_win, nomad)

        key = stdscr.getch()
        if key in command_dict:
            command_dict[key](nomad)

        update_entities(nomad, plains)

    stdscr.clear()
    stdscr.addstr(0, 0, "Game over.")
    stdscr.addstr(1, 0, "The nomad's journey has ended.") 
    stdscr.getch()
    curses.endwin()


def update_status_window(win, nomad):
    win.clear()
    y = 1
    x = 2
    ystep = 1

    win.addstr(y, x, '---- Nomad -----')
    y += ystep

    y += ystep
    win.addstr(y, x, 'Health: ')
    win.addstr('{:.0f}'.format(nomad.as_mortal.health))
    y += ystep
    win.addstr(y, x, 'Satiation: ')
    win.addstr('{:.0f}'.format(nomad.as_mortal.satiation))
    y += ystep

    y += ystep
    win.addstr(y, x, 'LH: ')
    win.addstr(str(nomad.as_tactile.left_held))
    y+= ystep
    win.addstr(y, x, 'RH: ')
    win.addstr(str(nomad.as_tactile.right_held))

    win.box()
    win.refresh()


def update_plains_window(win, display_dict, nomad, plains):
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


def update_entities(nomad, plains):
    for entity in plains.get_entities():
        entity.update(nomad)


def move_nomad(dx, dy, nomad):
    nomad.move(dx, dy)


def player_commands():
    def eat_underfoot(nomad):
        nomad.as_mortal.eat_underfoot()

    def pickup_underfoot(nomad):
        nomad.as_tactile.pickup_underfoot()

    def drop_all(nomad):
        nomad.as_tactile.drop_all()

    def make_tool(nomad):
        nomad.as_tactile.make_tool()

    return {
        #KEY('h'):  partial(move_nomad, *DIR_LEFT),
        #KEY('l'):  partial(move_nomad, *DIR_RIGHT),
        #KEY('k'):  partial(move_nomad, *DIR_UP),
        #KEY('j'):  partial(move_nomad, *DIR_DOWN),
        KEY_LEFT:   partial(move_nomad, *DIR_LEFT),
        KEY_RIGHT:  partial(move_nomad, *DIR_RIGHT),
        KEY_UP:     partial(move_nomad, *DIR_UP),
        KEY_DOWN:   partial(move_nomad, *DIR_DOWN),
        KEY('w'):   Nomad.wait,

        KEY('e'):   eat_underfoot,
        KEY('g'):   pickup_underfoot,
        KEY('d'):   drop_all,
        KEY('m'):   make_tool,
        }


def render_info():
    return {
        'nomad':        ('@', PAIR_YELLOW),
        'grass':        ('"', PAIR_GREEN),
        'flower':       ('*', PAIR_BLUE),
        'earth':        ('.', PAIR_WHITE),
        'rock':         ('0', PAIR_CYAN),
        'yak':          ('Y', PAIR_RED),
        'mushroom':     ('?', PAIR_MAGENTA),
        'sharp rock':   ('>', PAIR_CYAN),
        'stick':        ('/', PAIR_WHITE),
        'spear':        ('|', PAIR_YELLOW),
        }


def init_color_pairs():
    for (n, fg_color) in (
            (PAIR_RED,      curses.COLOR_RED),
            (PAIR_GREEN,    curses.COLOR_GREEN),
            (PAIR_YELLOW,   curses.COLOR_YELLOW),
            (PAIR_BLUE,     curses.COLOR_BLUE),
            (PAIR_MAGENTA,  curses.COLOR_MAGENTA),
            (PAIR_CYAN,     curses.COLOR_CYAN),
            (PAIR_WHITE,    curses.COLOR_WHITE)):
        curses.init_pair(n, fg_color, -1)
