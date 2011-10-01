#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys
from contextlib import closing

SOURCE_FILE = "word7.lst"
LENGTH = 7

def main():
    cutoff = ask_for_cutoff()
    stems = {}
    for word in words():
        stem_it(word, stems)
    for stem in stems:
        if stems[stem] < cutoff:
            continue
        print "%s: %d" % (stem, stems[stem]) 

def words():
    with closing(open(SOURCE_FILE)) as f:
        for line in f:
            yield line.strip()

def stem_it(word, stems):
    l = list(set(word))
    l.sort()
    ordered_chars = "".join(l)
    if len(ordered_chars) < LENGTH:
        return
    for c in ordered_chars:
        stem = ordered_chars.replace(c, "")
        stems.setdefault(stem, 0)
        stems[stem] += 1

def filter_list():
    name = sys.argv[1]
    max_len = LENGTH + 1 # len + \n
    with closing(open(name)) as fsource:
        with closing(open(SOURCE_FILE, "w")) as fout:
            for line in fsource:
                if len(line) != max_len or "'" in line:
                    continue
                else:
                    fout.write(line)
    print "Done"

def ask_for_cutoff():
    while True:
        str_cutoff = raw_input("Enter number of cutoff:\n")
        try:
            cutoff = int(str_cutoff)
            if cutoff > 0 and cutoff < 13:
                break
            else:
                print "Cutoff should be more then 0 and less then 13."
                print "Try again."
        except ValueError:
            pass
    return cutoff

if __name__ == "__main__":
    #filter_list()
    main()
