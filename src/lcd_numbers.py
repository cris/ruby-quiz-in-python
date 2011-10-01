#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import getopt
import sys
import itertools

carton = ('-', ('|', '|'), '-', ('|', '|'), '-')
" -- \n"
" --- "
"|  |\n|"
template = " %s \n%s%s%s\n%s%s%s\n"
digits = {
        '0': (1, 1, 1, 0, 1, 1, 1),
        '1': (0, 0, 1, 0, 0, 1, 0),
        '2': (1, 0, 1, 1, 1, 0, 1),
        '3': (1, 0, 1, 1, 0, 1, 1),
        '4': (0, 1, 1, 1, 0, 1, 0),
        '5': (1, 1, 0, 1, 0, 1, 1),
        '6': (1, 1, 0, 1, 1, 1, 1),
        '7': (1, 0, 1, 0, 0, 1, 0),
        '8': (1, 1, 1, 1, 1, 1, 1),
        '9': (1, 1, 1, 1, 0, 1, 1),
        }

def main():
    opts, numbers = getopt.gnu_getopt(sys.argv[1:], "s:")
    number = numbers[0]
    size = extract_size(opts)
    print_number(number, size)

def print_number(number, size):
    images = map(lambda n: prepare_num(n, size), number)
    for line in itertools.izip(*images):
        for p in line:
            print p,
        print
    print

def horizontal_line(flag, size):
    char = '-' if flag else ' '
    return " %s " % (char * size)

def vertical_line(flag1, flag2, size):
    bar1 = '|' if flag1 else ' '
    bar2 = '|' if flag2 else ' '
    space = ' ' * size
    return ["%s%s%s" % (bar1, space, bar2) for i in xrange(size)]
        

def digit_taker(array):
    for elem in array:
        yield elem
    

def prepare_num(c, size):
    digit = digits[c]
    take_digit = iter(digit).next
    rows = []
    rows.append(horizontal_line(take_digit(), size))
    rows.extend(vertical_line(take_digit(), take_digit(), size))
    rows.append(horizontal_line(take_digit(), size))
    rows.extend(vertical_line(take_digit(), take_digit(), size))
    rows.append(horizontal_line(take_digit(), size))
    return rows

def extract_size(opts):
    if len(opts) and opts[0][0] == '-s':
        size = int(opts[0][1])
    else:
        size = 2
    return size
        

if __name__ == "__main__":
    main()
