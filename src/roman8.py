#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys
import re

arabian_to_roman = {
        1:    "I",
        5:    "V",
        10:   "X",
        50:   "L",
        100:  "C",
        500:  "D",
        1000: "M",
        5000: "-",
        10000: "-"
        }
roman_to_arabian = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000
        }

def to_roman(number):
    snum = str(number)
    roman_list = []
    for i, c in enumerate(reversed(snum)):
        roman_list.append(_convert_digit(c, i))
    roman_list.reverse()
    return "".join(roman_list)

def to_arabian(snum):
    arabian_list = []
    degree = 0
    sum = 0
    for rnum in roman(snum):
        sum += _arabian_from_roman(rnum)
    return sum

def _arabian_from_roman(rnum):
    if len(rnum) == 1:
        return roman_to_arabian[rnum]
    if len(rnum) == 2:
        fdigit, sdigit = _to_arabian_sequence(rnum)
        if fdigit >= sdigit:
            return fdigit + sdigit
        else:
            return sdigit - fdigit
    if len(rnum) == 3:
        fdigit, sdigit, thdigit = _to_arabian_sequence(rnum)
        assert(sdigit == thdigit)
        return fdigit + sdigit + thdigit
    if len(rnum) == 4:
        fdigit, sdigit, thdigit, frdigit = _to_arabian_sequence(rnum)
        assert(sdigit == thdigit == frdigit)
        return fdigit + sdigit + thdigit + frdigit

def _to_arabian_sequence(string):
    l = list(string)
    return map(lambda c: roman_to_arabian[c], l)

def _return_roman(lchar):
    lchar.reverse()
    return "".join(lchar)

def roman(string):
    lchar = []
    for c in reversed(string):
        if not lchar:
            lchar.append(c)
        elif c == lchar[-1]:
            lchar.append(c)
        elif c != lchar[-1]:
            dprev = roman_to_arabian[lchar[-1]]
            dcurr = roman_to_arabian[c]
            if dcurr > dprev:
                yield _return_roman(lchar)
                lchar = [c]
            else:
                lchar.append(c)
                yield _return_roman(lchar)
                lchar = []
    if lchar:
        yield _return_roman(lchar)

def _convert_digit(char, num):
    digit = int(char)
    low, middle, high = _get_range(num)
    if digit == 0:
        return ""
    elif digit <= 3:
        return low * digit
    elif digit == 4:
        return low + middle
    elif digit == 5:
        return middle
    elif digit <= 8:
        return middle + low * (digit - 5)
    elif digit == 9:
        return low + high
    else:
        return high

def _get_range(order):
    low    = 10 ** order
    middle = low * 5
    high   = low * 10
    return arabian_to_roman[low], arabian_to_roman[middle], arabian_to_roman[high]

def _convert_to_inverse(line):
    if re.match(r'\d', line):
        result = to_roman(line.strip())
    else:
        result = to_arabian(line.strip())
    return str(result) + "\n"

def main():
    #for i in xrange(1, 4000):
        #rom = to_roman(i)
        #arab = to_arabian(rom)
        #print rom, arab
        #assert(i == arab)

    for line in sys.stdin:
        sys.stdout.write(_convert_to_inverse(line))
    #print "XLI", to_arabian("XLI")
    #print 234, to_roman(234)
    #print 1839, to_roman(1839)
    #print 2009, to_roman(2009)
    #print 1998, to_roman(1998)
    #print "CCXXXIV", to_arabian("CCXXXIV")
    #print "MDCCCXXXIX", to_arabian("MDCCCXXXIX")
    #print "MMIX", to_arabian("MMIX")
    #print "MCMXCVIII", to_arabian("MCMXCVIII")

if __name__ == "__main__":
    main()
