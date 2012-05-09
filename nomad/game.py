'''run the game'''
import curses
from curses import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN
from functools import partial

from nomad.entities import *
from nomad.nomad import Nomad
from nomad.plains import Plains
import nomad.plainsgen as gen
from nomad.util import *

# Subwindow dimensions as (height, width, y, x)
PLAINS_WIN = (21, 21, 1, 1)
STATUS_WIN = (21, 21, 0, 22)

# curses color pair numbers (for `init_color_pairs` and `render_info`)
PAIR_RED = 1
PAIR_GREEN = 2
PAIR_YELLOW = 3
PAIR_BLUE = 4
PAIR_MAGENTA = 5
PAIR_CYAN = 6
PAIR_WHITE = 7

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

    # Define the world.
    nomad = Nomad(los=6)
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
    plains.add_entity(nomad, 0, 0)

    # Initialize the user interface.
    plains_win = curses.newwin(*PLAINS_WIN) 
    status_win = curses.newwin(*STATUS_WIN)

    # Get rendering data.
    display_dict = render_info()
    # Get keybindings.
    command_dict = player_commands()
    # Execute the main loop while the nomad lives.
    while nomad.as_mortal.alive:
        # Update the screen.
        update_plains_window(plains_win, display_dict, plains)
        update_status_window(status_win, nomad)

        # Handle user input.
        key = stdscr.getch()
        if key in command_dict:
            command_dict[key](nomad)

        # Update all entities.
        update_entities(nomad, plains)

    # Game over.
    game_over(stdscr, nomad)


def update_status_window(win, nomad):
    '''Draw some information about a `Nomad` on a window.'''
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


def update_plains_window(win, display_dict, plains):
    '''Draw a `Plains` on a window, given rendering information.'''
    win.clear()

    coords = range(plains.entities.left, plains.entities.right + 1)
    # For y, x in the boundary rectangle of the plains
    for y in coords:
        for x in coords:
            # If xy is in the plains, draw the plains at that xy.
            if (x, y) in plains.entities:
                entity = plains.get_entity(x, y)
                char, color = display_dict[entity.name]
            # Otherwise, draw an blank space.
            else:
                char = ' '
                color = PAIR_WHITE
            win.addnstr(y + plains.entities.down, x + plains.entities.right,
                        char, 1, curses.color_pair(color))

    win.refresh()


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

    move_up = make_move_nomad(*DIR_UP)
    move_down = make_move_nomad(*DIR_DOWN)
    move_left = make_move_nomad(*DIR_LEFT)
    move_right = make_move_nomad(*DIR_RIGHT)
    move_upleft = make_move_nomad(*DIR_UPLEFT)
    move_upright = make_move_nomad(*DIR_UPRIGHT)
    move_downleft = make_move_nomad(*DIR_DOWNLEFT)
    move_downright = make_move_nomad(*DIR_DOWNRIGHT)

    def eat_underfoot(nomad):
        nomad.as_mortal.eat_underfoot()

    def pickup_underfoot(nomad):
        nomad.as_tactile.pickup_underfoot()

    def drop_all(nomad):
        nomad.as_tactile.drop_all()

    def make_tool(nomad):
        nomad.as_tactile.make_tool()

    def multikey_dict(d):
        return dict((key, v) for keys, v in d.items() for key in keys)

    KEY = ord

    return multikey_dict({
        (KEY('k'), KEY_UP):    move_up,
        (KEY('j'), KEY_DOWN):  move_down,
        (KEY('h'), KEY_LEFT):  move_left,
        (KEY('l'), KEY_RIGHT): move_right,
        (KEY('y'),):           move_upleft,
        (KEY('u'),):           move_upright,
        (KEY('b'),):           move_downleft,
        (KEY('n'),):           move_downright,

        (KEY('w'),): Nomad.wait,
        (KEY('e'),): eat_underfoot,
        (KEY('g'),): pickup_underfoot,
        (KEY('d'),): drop_all,
        (KEY('m'),): make_tool,
        })


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
