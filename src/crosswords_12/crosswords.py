#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys


def each_position(llist):
    for y, line in enumerate(llist):
        for x, c in enumerate(line):
            yield (x, y), c

EMPTY = ' '
BLACK = 'X'
PLACE = '_'

class Crossword:
    move_matrix = {
            'top': (0, -1),
            'bottom': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
            }
    black_matrix = [
            ['#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#'],
            ['#', '#', '#', '#', '#', '#'],
            ]
    place_matrix = [
            ['#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#'],
            ]

    def __init__(self, layout):
        self.layout = layout
        self.max_y  = len(layout) - 1
        self.max_x  = len(layout[0]) - 1

    def __iter__(self):
        return iter(self.layout)

    def __str__(self):
        return "\n".join(repr(line) for line in self.layout)

    def _get(self, (x, y)):
        if self._is_correct_position((x, y)):
            return self.layout[y][x]
        else:
            return None

    def _set(self, (x, y), c):
        self.layout[y][x] = c
        return self

    def _is_on_border(self, (x, y)):
        if y == 0 or y == self.max_y:
            return True
        elif x == 0 or x == self.max_x:
            return True
        else:
            return False

    def _near_empty(self, position):
        nearests = self._get_nearests(position)
        for (x,y), c in nearests:
            if c == EMPTY:
                return True
        return False

    def _get_nearests(self, (x, y)):
        coords = [(x + d_x, y + d_y) for d_x, d_y in self.move_matrix.values()]
        return [(pos, self._get(pos)) for pos in coords if self._is_correct_position(pos)]

    def _is_correct_position(self, (x, y)):
        if 0 <= x <= self.max_x and 0 <= y <= self.max_y:
            return True
        else:
            return False

    def find_holes(self):
        try_again = True
        while try_again:
            try_again = False
            for pos, c in each_position(self):
                if c == BLACK and (self._is_on_border(pos) or self._near_empty(pos)):
                    try_again = True
                    self._set(pos, EMPTY)

    def fill_numbers(self):
        number = 1
        for pos, c in each_position(self):
            if self._should_have_number(pos, c):
                self._set(pos, number)
                number += 1

    def _near(self, direction, (x, y)):
        d_x, d_y = self.move_matrix[direction]
        return self._get((x + d_x, y + d_y))

    def _should_have_number(self, position, char):
        if char == PLACE and self._is_good_for_number(position):
            return True
        else:
            return False

    def _is_good_for_number(self, position):
        if self._near('top', position) in [None, EMPTY, BLACK] and self._near('bottom', position) == PLACE:
            return True
        elif self._near('left', position) in [None, EMPTY, BLACK] and self._near('right', position) == PLACE:
            return True
        return False

    def render(self):
        screen = self._prepare_screen()
        for pos, c in each_position(self):
            self._render_char(screen, pos, c)
        self._render_screen(screen)

    def _render_screen(self, screen):
        for line in screen:
            for c in line:
                sys.stdout.write(c)
            print


    def _render_char(self, screen, position, char):
        if char == EMPTY:
            return
        elif char == BLACK:
            self._render_black(screen, position)
        elif char == PLACE or isinstance(char, int):
            self._render_place(screen, position, char)

    def _render_place(self, screen, position, char):
        self._render_raw_place(screen, position)
        if isinstance(char, int):
            self._render_number(screen, position, char)

    def _render_number(self, screen, (x, y), number):
        snum = str(number)
        #s_position = (x + 1, y + 1)
        screen_x = self._x_on_screen(x)
        screen[self._y_on_screen(y)+1][(screen_x + 1):(screen_x + len(snum))] = snum


    def _render_raw_place(self, screen, position):
        self._render_box(screen, position, self.place_matrix)

    def _render_black(self, screen, position):
        self._render_box(screen, position, self.black_matrix)

    def _x_on_screen(self, x):
        return x * 5

    def _y_on_screen(self, y):
        return y * 3

    def _render_box(self, screen, (x, y), box):
        y_min = y * 3
        y_till = (y + 1) * 3 + 1
        for i, line in enumerate(screen[y_min:y_till]):
            x_min = x * 5
            x_till = (x + 1) * 5 + 1
            line[x_min:x_till] = box[i]


    def _prepare_screen(self):
        return [[' ' for _x in xrange(self._render_x_size())] for _y in xrange(self._render_y_size())]

    def _render_y_size(self):
        return (self.max_y + 1) * 3 + 1

    def _render_x_size(self):
        return (self.max_x + 1) * 5 + 1



def _main(fname):
    crossword = _read_crossword(fname)
    crossword.find_holes()
    crossword.fill_numbers()
    crossword.render()


def _read_crossword(fname):
    with open(fname) as f:
        llist = [[c for c in line if c in ['_', 'X']] for line in f]
        return Crossword(llist)

def main():
    if not sys.argv[1]:
        print "Provide file with crossword."
        sys.exit(1)
    _main(sys.argv[1])

if __name__ == "__main__":
    main()
