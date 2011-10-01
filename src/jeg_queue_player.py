#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from rock_paper_scissors import Player

class JEGQueuePlayer(Player):
    QUEUE = ['rock', 'scissors', 'scissors']

    def __init__(self, opponent_name):
        super(self.__class__, self).__init__(opponent_name)
        self.index = 0

    def choose(self):
        choice = self.QUEUE[self.index]
        self.index += 1
        if self.index == len(self.QUEUE):
            self.index = 0
        return choice

