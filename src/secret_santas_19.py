#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import random,sys


def set_santa(players):
    while True:
        pairs = _set_santa(players)
        if pairs:
            return pairs

def _set_santa(players):
    free_players = players[:]
    pairs = []
    for p in players:
        current_free_players = free_players[:]
        while True:
            if current_free_players == []:
                return False
            receiver = random.choice(current_free_players)
            if p != receiver and p[1] != receiver[1]:
                pairs.append((p, receiver))
                free_players.remove(receiver)
                break
            else:
                current_free_players.remove(receiver)
    return pairs

def main():
    players = []
    for line in sys.stdin:
        fname, lname = line.split()
        players.append((fname, lname))
    santa_list = set_santa(players)
    for santa, receiver in santa_list:
        print santa[0], santa[1], "\t\t", receiver[0], receiver[1]


if __name__ == "__main__":
    main()
