#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import string
import pdb

SONGS = [
    "Peace Train",
    "No More I Love You's",
    "Super Trooper",
    "Rock Me, Amadeus",
    "Song of the South",
    "Hooked on a Feeling",
    "Go Tell It on the Mountain"
]

def build_chain(first, last, songs):
    last_of_first = _last_char(first)
    first_of_last = _first_char(last)
    if last_of_first == first_of_last:
        return [first, last]
    else:
        between_songs = _find_between([[first]], last, songs)
        between_songs.append(last)
        return between_songs

def _find_between(states, last_song, songs):
    lchar = _first_char(last_song)
    counter = 0
    while counter < 4:
        new_states = []
        for state in states:
            next_level_songs = []
            fchar = _last_char(state[-1])
            for song in songs:
                if song in state or song == last_song:
                    continue
                if _match_both(song, fchar, lchar):
                    state.append(song)
                    return state
                elif _match_first(song, fchar):
                    next_level_songs.append(song)
            add_new_states(new_states, state, next_level_songs)
        counter += 1
        states = new_states
    return []


def add_new_states(new_states, state, next_level_songs):
    for song in next_level_songs:
        new_state = state[:]
        new_state.append(song)
        new_states.append(new_state)

def _match_first(song, fchar):
    return _first_char(song) == fchar

def _match_both(song, fchar, lchar):
    return _first_char(song) == fchar and _last_char(song) == lchar


def _prepare_songs(songs):
    prepared_songs = {}
    for song in songs:
        prepared_songs[song] = (_first_char(song), _last_char(song))
    return prepared_songs

def _first_char(song):
    for c in song:
        if c.isalpha():
            return c.lower()

def _last_char(song):
    for c in reversed(song):
        if c.isalpha():
            return c.lower()


def main():
    #prepared_songs = _prepare_songs(SONGS)
    chain = build_chain("Peace Train", "Go Tell It on the Mountain", SONGS)
    print chain

if __name__ == "__main__":
    main()
