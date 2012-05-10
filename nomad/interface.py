import curses

from nomad.util import *

# curses color pair numbers (for `init_color_pairs` and `render_info`)
PAIR_RED = 1
PAIR_GREEN = 2
PAIR_YELLOW = 3
PAIR_BLUE = 4
PAIR_MAGENTA = 5
PAIR_CYAN = 6
PAIR_WHITE = 7

ui = None

class Interface:

    def __init__(self, stdscr, plains_win, status_win, nomad, display_dict):
        self.stdscr = stdscr
        self.plains_win = plains_win
        self.status_win = status_win
        self.nomad = nomad
        self.display_dict = display_dict

        self.dir_selector =  {
                ord('s'): (0, 0),
                ord('h'): DIR_LEFT,
                ord('j'): DIR_DOWN,
                ord('k'): DIR_UP,
                ord('l'): DIR_RIGHT,
                ord('y'): DIR_UPLEFT,
                ord('u'): DIR_UPRIGHT,
                ord('b'): DIR_DOWNLEFT,
                ord('n'): DIR_DOWNRIGHT,}

    @property
    def plains(self):
        return self.nomad.plains

    def select_adjacent_entity(self, *dirs):
        los = self.nomad.los
        x, y = self.nomad.pos
        self.plains_win.chgat(y + los, x + los, 1, curses.A_REVERSE)
        cmd = None
        while True:
            cmd = self.plains_win.getch()
            if cmd not in self.dir_selector:
                continue

            self.update_plains_window()
            dx, dy = self.dir_selector[cmd]
            self.plains_win.chgat(y + los, x + los, 1, curses.A_REVERSE)

            if (dx, dy) == (0, 0):
                return self.nomad.get_underfoot()
            else:
                adjacent = self.nomad.get_adjacent(dx, dy)
                if not adjacent.walkable:
                    return adjacent
                else:
                    return None

                    
    def update_status_window(self):
        '''Draw some information about a `Nomad` on a window.'''
        self.status_win.clear()
        y = 1
        x = 2
        ystep = 1

        self.status_win.addstr(y, x, '---- Nomad -----')
        y += ystep

        y += ystep
        self.status_win.addstr(y, x, 'Health: ')
        self.status_win.addstr('{:.0f}'.format(self.nomad.as_mortal.health))
        y += ystep
        self.status_win.addstr(y, x, 'Satiation: ')
        self.status_win.addstr('{:.0f}'.format(self.nomad.as_mortal.satiation))
        y += ystep

        y += ystep
        self.status_win.addstr(y, x, 'LH: ')
        self.status_win.addstr(str(self.nomad.as_tactile.held_entities[0]))
        y+= ystep
        self.status_win.addstr(y, x, 'RH: ')
        self.status_win.addstr(str(self.nomad.as_tactile.held_entities[1]))

        self.status_win.box()
        self.status_win.refresh()


    def update_plains_window(self):
        '''Draw a `Plains` on a window, given rendering information.'''
        self.plains_win.clear()

        coords = range(self.plains.entities.left, self.plains.entities.right + 1)
        # For y, x in the boundary rectangle of the plains
        for y in coords:
            for x in coords:
                # If xy is in the plains, draw the plains at that xy.
                if (x, y) in self.plains.entities:
                    entity = self.plains.get_entity(x, y, -1)
                    char, color = self.display_dict[entity.name]
                # Otherwise, draw an blank space.
                else:
                    char = ' '
                    color = PAIR_WHITE
                self.plains_win.addnstr(y + self.plains.entities.down,
                                        x + self.plains.entities.right,
                            char, 1, curses.color_pair(color))

        self.plains_win.refresh()
