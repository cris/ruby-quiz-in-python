#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys, os


class Player(object):
    players = []

    @classmethod
    def inherited(cls, player):
        cls.players.append(player)

    @classmethod
    def each_pair(cls):
        for i in xrange(len(cls.players)-1):
            for j in xrange(i+1, len(cls.players)):
                yield cls.get_class_from_module(cls.players[i]), cls.get_class_from_module(cls.players[j])

    @classmethod
    def get_class_from_module(cls, module):
        l = [v for v in module.__dict__.values() if isinstance(v, type)]
        return l[0]

    def __init__(self, opponent_name):
        print opponent_name
        self.opponent_name = opponent_name

    def choose(self):
        raise NotImplemented("Player subclasses must override choose().")

    def result(self, your_choice, opponent_choice, win_lose_or_draw):
        pass

class Game:
    def __init__(self, player1, player2):
        self.player1_name = str(player1)
        self.player2_name = str(player2)
        self.player1 = player1(self.player2_name)
        self.player2 = player2(self.player1_name)
        self.score1 = 0
        self.score2 = 0

    def play(self, num_matches):
        for i in xrange(num_matches):
            hand1 = self.player1.choose()
            hand2 = self.player2.choose()

            for player, hand in [(self.player1_name, hand1), (self.player2_name, hand2)]:
                if hand not in ['rock', 'paper', 'scissors']:
                    raise ValueError("Invalid choice by %s" % player)

            hands = {str(hand1): self.player1, str(hand2): self.player2}
            choices = hands.keys()
            choices.sort()
            if len(choices) == 1:
                self._draw(hand1, hand2)
            elif choices == ['paper', 'rock']:
                self._win(hands['paper'], hand1, hand2)
            elif choices == ['rock', 'scissors']:
                self._win(hands['rock'], hand1, hand2)
            elif choices == ['paper', 'scissors']:
                self._win(hands['scissors'], hand1, hand2)

    def results(self):
        match = "%s vs. %s\n\t%s: %s\n\t%s: %s\n" % (self.player1_name, self.player2_name, self.player1_name, self.score1, self.player2_name, self.score2)
        if self.score1 == self.score2:
            match + "\tDraw\n"
        elif self.score1 > self.score2:
            match + ("\t%s Wins\n" % self.player1_name)
        else:
            match + ("\t%s Wins\n" % self.player2_name)
        return match

    def _draw(self, hand1, hand2):
        self.score1 += 0.5
        self.score2 += 0.5
        self.player1.result(hand1, hand2, 'draw')
        self.player2.result(hand2, hand1, 'draw')

    def _win(self, winner, hand1, hand2):
        if winner == self.player1:
            self.score1 += 1
            self.player1.result(hand1, hand2, 'win')
            self.player2.result(hand2, hand1, 'lose')
        else:
            self.score2 += 1
            self.player1.result(hand1, hand2, 'lose')
            self.player2.result(hand2, hand1, 'win')

def main():
    match_game_count = 1000
    players_files = sys.argv[1:]
    if len(sys.argv) > 2 and sys.argv[1] == "-m" and re.match(r'/^[1-9]\d*$', sys.argv[2]):
        match_game_count = int(sys.argv[2])
        players_files = sys.argv[3:]

    print players_files
    for fname in players_files:
        print fname
        file_name = os.path.basename(fname)
        module_name, _ext = os.path.splitext(file_name)
        module = __import__(module_name)
        Player.inherited(module)

    for one, two in Player.each_pair():
        game = Game(one, two)
        game.play(match_game_count)
        print game.results()

if __name__ == "__main__":
    main()
