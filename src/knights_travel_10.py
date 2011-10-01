#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from sys import argv
from sys import exit

_move_star = [(1, 2), (2, 1), (2, -1), (1, -2),
              (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

count = 0

def calculate_travel(start, end, forbidden):
    all_pathes = []
    _do(start, end, forbidden, all_pathes, None)
    return all_pathes

def max_call(number, name):
    def max_call_number(fun):
        hack_i = [0]
        def max_call_number_do(*args, **kwargs):
            print "*" * 50, hack_i[0], name
            if hack_i[0] < number:
                hack_i[0] += 1
                return fun(*args, **kwargs)
            else:
                return
        return max_call_number_do
    return max_call_number

def _do(start, end, _forbidden, all_pathes, _current_path=None):
    global count
    #if count > 10000:
        #exit()
    #else:
        #count += 1
    forbidden = _forbidden[:]
    current_path = _current_path[:] if _current_path else []
    #if _current_path and len(_current_path) > 6:
        #print "HHHH"
        #return
    current_path.append(start)
    nearests = _allowed_nearests(start, forbidden)
    print all_pathes
    print "S: %s" % str(start)
    print "E: %s" % str(end)
    print "N: %s" % nearests
    print "F: %s %s" % (id(forbidden), forbidden)
    print "CF: %s %s" % (id(current_path), current_path)
    #if _current_path and len(_current_path) > 6:
        #print "HHHH"
        #return
    if start == end:
        print "S: %s" % str(start)
        print "E: %s" % str(end)
        all_pathes.append(current_path)
        print "A: %s" % all_pathes
        #exit()
        #del current_path[:]
        return
    full_forbidden = list(set(forbidden) | set(nearests))
    for pos in nearests:
        _do(pos, end, full_forbidden, all_pathes, current_path)

def _allowed_nearests(position, forbidden):
    nearests = _find_nearest(position)
    allowed_nearests = []
    for pos in nearests:
        try:
            forbidden.index(pos)
        except ValueError:
            allowed_nearests.append(pos)
    return allowed_nearests


def _find_nearest((x, y)):
    nearests = []
    for inc_x, inc_y in _move_star:
        near_x, near_y = (inc_x + x), (inc_y + y)
        if near_x <= 0 or near_y <= 0 or near_x > 8 or near_y > 8:
            continue
        nearests.append((near_x, near_y))
    return nearests

def _to_dec(string):
    x = ord(string[0]) - ord('a') + 1
    y = int(string[1])
    return x,y

def _to_alg(x, y):
    return str(x + 1) + str(y + 1)


def main():
    start, end = _to_dec(argv[1]), _to_dec(argv[2])
    forbidden = map(_to_dec, argv[3:])
    all = calculate_travel(start, end, forbidden)
    print min(all, key=len)

if __name__ == "__main__":
    main()
