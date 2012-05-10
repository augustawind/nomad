'''run the game'''
import curses
from curses import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN
from functools import partial

from nomad.entities import *
from nomad import interface
from nomad.interface import *
from nomad.nomad import Nomad
from nomad.plains import Plains
import nomad.plainsgen as gen
from nomad.util import *

# Subwindow dimensions as (height, width, y, x)
PLAINS_WIN = (21, 21, 1, 1)
STATUS_WIN = (21, 21, 0, 22)


def run():
    '''Initialize curses and call `main`.'''
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    curses.wrapper(main)
    curses.curs_set(1)


def main(stdscr): 
    '''Run the game, given a curses ``stdscr``.'''
    init_color_pairs()

    # Define the nomad.
    nomad = Nomad(los=6)
    # Define the plains.
    los = nomad.los
    half_los = los // 2 + 1
    plains = Plains.with_floor(earth,
                               gen.chance(
                                   {90: grass, 10: flower,
                                    3: mushroom, 5: stick,
                                    2: sharp_rock, 1: yak}),
                               up=-los, left=-los, right=los, down=los,
                               ul=Point(-half_los, -half_los),
                               ur=Point(-half_los, half_los),
                               lr=Point(half_los, half_los),
                               ll=Point(half_los, -half_los),)
    # Add nomad to plains.
    plains.add_entity(nomad, 0, 0)

    # Make windows.
    plains_win = curses.newwin(*PLAINS_WIN) 
    status_win = curses.newwin(*STATUS_WIN)
    # Get rendering data.
    display_dict = render_info()
    # Get keybindings.
    command_dict = player_commands()
    # Initialize user interface.
    interface.ui = interface.Interface(stdscr, plains_win, status_win,
                                       nomad, display_dict, command_dict)

    # Execute the main loop while the nomad lives.
    while nomad.as_mortal.alive:
        # Update the screen.
        interface.ui.update_plains_window()
        interface.ui.update_status_window()

        # Get and handle user input.
        interface.ui.interact()

        # Update all entities.
        update_entities(nomad, plains)

    # Game over.
    game_over(stdscr, nomad)


def update_entities(nomad, plains):
    '''Update each `Entity` in the `Plains` with the `Nomad`.'''
    for entity in plains.get_entities():
        entity.update(nomad)


def game_over(stdscr, nomad):
    '''End the game.'''
    stdscr.clear()
    stdscr.addstr(0, 0, "Game over.")
    stdscr.addstr(1, 0, "The nomad's journey has ended.") 
    stdscr.getch()
    curses.endwin()


def player_commands():
    '''Return a dict mapping curses key values to functions that
    should be called when those keys are pressed.

    Each function should take a `Nomad` as its single argument.
    '''

    def make_move_nomad(dx, dy):
        def move_nomad(nomad):
            nomad.move(dx, dy)
        return move_nomad

    # Assign movement keys (from `interface.key_to_dir`).
    commands = dict((key, make_move_nomad(*d))
                    for key, d in key_to_dir.items())

    def eat_nearest(nomad):
        nomad.as_tactile.eat_nearest()

    def pickup_nearest(nomad):
        nomad.as_tactile.pickup_nearest()

    def drop_all(nomad):
        nomad.as_tactile.drop_all()

    def combine_objects(nomad):
        nomad.as_tactile.combine_objects()

    # Assign all other single-key actions.
    commands.update({
        ord('w'): Nomad.wait,
        ord('e'): eat_nearest,
        ord('g'): pickup_nearest,
        ord('d'): drop_all,
        ord('c'): combine_objects,
        })

    return commands


def render_info():
    '''Return a dict mapping entity names to rendering data.

    Each value is of the form (char, pair_num) where char is the
    character to render and pair_num is a curses color pair number 0-9.
    '''
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
    '''Initialize curses color pairs.'''
    for (n, fg_color) in (
            (PAIR_RED,      curses.COLOR_RED),
            (PAIR_GREEN,    curses.COLOR_GREEN),
            (PAIR_YELLOW,   curses.COLOR_YELLOW),
            (PAIR_BLUE,     curses.COLOR_BLUE),
            (PAIR_MAGENTA,  curses.COLOR_MAGENTA),
            (PAIR_CYAN,     curses.COLOR_CYAN),
            (PAIR_WHITE,    curses.COLOR_WHITE)):
        curses.init_pair(n, fg_color, -1)
