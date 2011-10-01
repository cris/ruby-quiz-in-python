#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import pdb
import curses

def each_position(llist):
    for y, line in enumerate(llist):
        for x, c in enumerate(line):
            yield (x, y), c

class Controller:
    def __init__(self, view, control):
        self.game = Sokoban()
        init_state = self.game.initial_state()
        self.view = view
        self.view.init(init_state)
        self.control = control

    def start(self):
        self._loop()

    def _loop(self):
        while True:
            command = self.control.read_command()
            state_update = self.game.process(command)
            if state_update == 'exit':
                break
            if state_update == 'win':
                self.view.thewin()
                break
            else:
                self.view.update(state_update)

WALL = '#'
EMPTY = ' '
PLAYER = '@'
CRATE = 'o'
STORAGE = '.'
CRATE_ON_STORAGE = '*'
PLAYER_ON_STORAGE = '+'

class Sokoban:
    level = [
            [WALL, WALL,    WALL,  WALL,  WALL,  WALL],
            [WALL, PLAYER_ON_STORAGE,  EMPTY, EMPTY, EMPTY, WALL],
            [WALL, CRATE_ON_STORAGE,   EMPTY, EMPTY, EMPTY, WALL],
            [WALL, EMPTY,   EMPTY, EMPTY, EMPTY, WALL],
            [WALL, EMPTY,   CRATE, EMPTY, EMPTY, WALL],
            [WALL, EMPTY,   EMPTY, EMPTY, EMPTY, WALL],
            [WALL, STORAGE, EMPTY, EMPTY, EMPTY, WALL],
            [WALL, WALL,    WALL,  WALL,  WALL,  WALL],
            ]
    move_matrix = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
            }
    moves = move_matrix.keys()
    apply_matrix = {
            PLAYER: {
                EMPTY: PLAYER,
                STORAGE: PLAYER_ON_STORAGE
                },
            CRATE: {
                EMPTY: CRATE,
                STORAGE: CRATE_ON_STORAGE
                }
            }


    def __init__(self):
        self.position = self._initial_position(self.level)
        self.static_scene = self._static_scene(self.level)
        pass

    def initial_state(self):
        return self.level

    def process(self, command):
        if self._all_crates_on_storages():
            return 'win'
        if command in self.moves:
            state_update = self._move_to(command)
        elif command == 'exit':
            state_update = command
        return state_update

    def _all_crates_on_storages(self):
        for (x,y), c in each_position(self.level):
            if c == CRATE:
                return False
        return True


    def _initial_position(self, level):
        for (x,y), c in each_position(level):
            if c == PLAYER or c == PLAYER_ON_STORAGE:
                return x, y

    def _static_scene(self, level):
        return [[self._extract_static_info(c) for c in line] for line in level]

    def _extract_static_info(self, char):
        if char in [WALL, STORAGE, EMPTY]:
            return char
        elif char in [CRATE_ON_STORAGE, PLAYER_ON_STORAGE]:
            return STORAGE
        elif char in [PLAYER, CRATE]:
            return EMPTY


    def _crates(self, level):
        for (x,y), c in each_position(level):
            if c == CRATE or c == CRATE_ON_STORAGE:
                return x, y

    def _move_to(self, direction):
        d_x, d_y = self.move_matrix[direction]
        new_position = (self.position[0] + d_x, self.position[1] + d_y)
        next_to_new_position = (new_position[0] + d_x, new_position[1] + d_y)
        if self._can_move_to(new_position, next_to_new_position):
            state_update = self._move(self.position, new_position, next_to_new_position)
            return state_update
        else:
            return []

    def _level_set(self, (pos_x, pos_y), value):
        self.level[pos_y][pos_x] = value

    def _level_get(self, (pos_x, pos_y)):
        return self.level[pos_y][pos_x]

    def _static_scene_get(self, (pos_x, pos_y), new_element=None):
        bottom_element = self.static_scene[pos_y][pos_x]
        if new_element:
            return self.apply_matrix[new_element][bottom_element]
        else:
            return bottom_element

    def _level_update(self, state_update):
        for pos, v in state_update:
            self._level_set(pos, v)

    def _move(self, old_position, new_position, next_to_new_position):
        self.position = new_position
        old_position_element = self._static_scene_get(old_position)
        new_position_element = self._static_scene_get(new_position, PLAYER)
        state_update = [(old_position, old_position_element),
                (new_position, new_position_element)]
        if self._level_get(new_position) in [CRATE, CRATE_ON_STORAGE]:
            next_to_new_position_element = self._static_scene_get(next_to_new_position, CRATE)
            state_update.append((next_to_new_position, next_to_new_position_element))
        self._level_update(state_update)
        return state_update

    def _can_move_to(self, position, next_position):
        item_at_position = self._level_get(position)
        item_at_next_position = self._level_get(next_position)

        if item_at_position == EMPTY or item_at_position == STORAGE:
            return True
        elif item_at_position in [CRATE, CRATE_ON_STORAGE] and item_at_next_position in [EMPTY, STORAGE]:
            return True
        else:
            curses.beep()
            return False


class KeyReader:
    key_binding = {
            curses.KEY_UP     : 'up',
            curses.KEY_DOWN   : 'down',
            curses.KEY_RIGHT  : 'right',
            curses.KEY_LEFT   : 'left',
            27 : 'exit' # Escape
            }
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def read_command(self):
        while True:
            c = self.stdscr.getch()
            if c in self.key_binding:
                return self.key_binding[c]

class SimpleView:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def init(self, screen):
        self.win = self._create_new_win(len(screen), len(screen[0]))
        self._init_win(self.win, screen)
        self._refresh()

    def _init_win(self, win, screen):
        #for line in screen:
            #win.addstr("".join(line))
            #win.addch("\n")
        for (x,y),c in each_position(screen):
            win.addch(y, x, c)

    def _create_new_win(self, height, width):
        begin_y, begin_x = 0, 0
        win = curses.newpad(height+1, width+1)
        return win

    def _refresh(self):
        self.win.refresh(0,0, 0,0, 10,10)

    def thewin(self):
        self.win.addstr("POBEDA!")
        self._refresh()

    def update(self, state_update):
        for (x, y), c in state_update:
            self.win.addch(y, x, ord(c))
        self._refresh()

def main():
    curses.wrapper(_main)

def _main(stdscr):
    _init_curses(stdscr)
    view = SimpleView(stdscr)
    control = KeyReader(stdscr)
    Controller(view, control).start()
    _terminate_curses(stdscr)

def _init_curses(stdscr):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)

def _terminate_curses(stdscr):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.curs_set(1)
    curses.endwin()


if __name__ == "__main__":
    main()
