#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from rock_paper_scissors import Player

class CrisAiPlayer(Player):
    def __init__(self, opponent_name):
        super(self.__class__, self).__init__(opponent_name)
        self.wins = {
                'rock': 0,
                'paper': 0,
                'scissors': 0
        }

    def choose(self):
        res = self._max_from_dict(self.wins)
        #print self.wins
        #print res
        return res

    def result(self, your_choice, opponents_choice, win_lose_draw):
        if win_lose_draw == 'win':
            self.wins[your_choice] += 1
        elif win_lose_draw == 'loose':
            win_key = self._another_one(your_choice, opponents_choice)
            self.wins[win_key] += 1
        else:
            win_key = self._another_one(your_choice, opponents_choice)
            self.wins[win_key] += 1

    def _another_one(self, fchoice, schoice):
        return filter(lambda x: x != fchoice and x != schoice, self.wins.keys())[0]

    def _max_from_dict(self, dct):
        max_k, max_v = dct.items()[0]
        for k in dct:
            if dct[k] > max_v:
                max_v = dct[k]
                max_k = k
        return max_k


