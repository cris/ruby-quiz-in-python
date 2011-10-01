#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import random

FACES = "AKQJT98765432"
SUITS = "cdhs"

deck = [face + suit for face in FACES for suit in SUITS]

random.shuffle(deck)

common = [deck.pop() for _i in xrange(5)]

hole = [[deck.pop() for _i1 in xrange(2)] for _i2 in xrange(8)]

hands = []
all_fold = True
while all_fold:
    hands = []
    for h in hole:
        num_common = random.choice([0, 3, 4, 5])
        if num_common == 5:
            all_fold = False
        if num_common > 0:
            hand = h + common[:num_common]
        else:
            hand = h
        hands.append(" ".join(hand))

for h in hands:
    print h

