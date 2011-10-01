#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys


class Hand(object):
    FACES = "AKQJT98765432"
    SUITS = "cdhs"
    HANDS = {
        'royal_flush'     : "Royal flush",
        'straight_flush'  : "Straight flush",
        'four_of_a_kind'  : "Four of a kind",
        'full_house'      : "Full house",
        'flush'           : "Flush",
        'straight'        : "Straight",
        'three_of_a_kind' : "Three of a kind",
        'two_pair'        : "Two pair",
        'pair'            : "Pair",
        'high_card'       : "High card"
    }

    HANDS_KEYS = ['royal_flush', 'straight_flush', 'four_of_a_kind',
            'full_house', 'flush', 'straight', 'three_of_a_kind',
            'two_pair', 'pair', 'high_card'
    ]

    def __init__(self, number, cards):
        self.number = number
        self.cards = self._extract_cards(cards)
        self.hand = self._appraise_hand(self.cards)

    def _appraise_hand(self, cards):
        for h in self.HANDS_KEYS:
            fname = "_is_%s" % h
            result = getattr(self, fname)(cards)
            if result:
                return result

    def _is_royal_flush(self, cards):
        straight_flush = self._try_to_build_straight_flush(cards)
        if straight_flush and straight_flush[0][0] == self._face('A'):
            return ('royal_flush', [], [])
        else:
            return False

    def _is_straight_flush(self, cards):
        straight_flush = self._try_to_build_straight_flush(cards)
        if straight_flush:
            return ('straight_flush', [straight_flush[0]], [])
        else:
            return False

    def _is_four_of_a_kind(self, cards):
        max_faces = self._max_faces(cards)
        if len(max_faces[0]) == 4:
            max_face_in_cards = max_faces[0][0][0]
            max_kickers = self._max_kickers(cards, except_cards=max_faces[0])
            return ('four_of_a_kind', [max_face_in_cards], max_kickers)
        else:
            return False

    def _is_full_house(self, cards):
        max_faces = self._max_faces(cards)
        if len(max_faces[0]) == 3 and len(max_faces[1]) >= 2:
            max_face1, max_face2 = max_faces[0][0][0], max_faces[1][0][0]
            return ('full_house', [max_face1, max_face2], [])
        else:
            return False

    def _is_flush(self, cards):
        same_suit_cards = self._same_suit_cards(cards)
        if len(same_suit_cards) < 5:
            return False
        else:
            return ('flush', [same_suit_cards[0][0]], [])

    def _is_straight(self, cards):
        seq = self._try_to_build_straight(cards)
        if seq:
            return ('straight', [seq[0][0]], [])
        else:
            return False

    def _is_three_of_a_kind(self, cards):
        max_faces = self._max_faces(cards)
        if len(max_faces[0]) == 3:
            max_face_in_cards = max_faces[0][0][0]
            max_kickers = self._max_kickers(cards, except_cards=max_faces[0])
            return ('three_of_a_kind', [max_face_in_cards], max_kickers)
        else:
            return False

    def _is_two_pair(self, cards):
        max_faces = self._max_faces(cards)
        if len(max_faces[0]) == 2 and len(max_faces[1]) == 2:
            max_face1, max_face2 = max_faces[0][0][0], max_faces[1][0][0]
            excepts = max_faces[0][:]
            excepts.extend(max_faces[1])
            max_kickers = self._max_kickers(cards, except_cards=excepts)
            return ('two_pair', [max_face1, max_face2], max_kickers)
        else:
            return False

    def _is_pair(self, cards):
        max_faces = self._max_faces(cards)
        if len(max_faces[0]) == 2:
            max_face = max_faces[0][0][0]
            max_kickers = self._max_kickers(cards, except_cards=max_faces[0])
            return ('pair', [max_face], max_kickers)
        else:
            return False

    def _is_high_card(self, cards):
        return ('high_card', self._max_kickers(cards))

    def _has_ace(self, cards):
        ace = self._face('A')
        for f, _s in cards:
            if ace == f:
                return True 
        return False

    def _max_faces(self, cards):
        kinds = [[] for _i in xrange(len(self.FACES))]
        for f, s in cards:
            kinds[f].append((f,s))
        # sort by len
        kinds.sort(cmp=self._cmp_seq, reverse=True)
        return kinds

    def _cmp_seq(self, x, y):
        if len(x) != len(y):
            return cmp(len(x), len(y))
        else:
            if not x:
                return 0
            else:
                return -cmp(x[0], y[0])

    def _try_to_build_straight_flush(self, cards):
        same_suit_cards = self._same_suit_cards(cards)
        if len(same_suit_cards) < 5:
            return False
        straight = self._try_to_build_straight(same_suit_cards)
        return straight

    def _try_to_build_straight(self, cards):
        card_sequence = self._longest_sequence(cards)
        if len(card_sequence) >= 5:
            return card_sequence[:5]
        elif len(card_sequence) == 4 and card_sequence[0][0] == self._face('5') and self._contain_face(cards, self._face('A')):
            low_straight = card_sequence
            low_straight.append((self._face('A'), card_sequence[0][1]))
            return low_straight
        else:
            return False

    def _max_kickers(self, cards, except_cards=[]):
        #FIXME: change set on diff between lists
        rest_cards = cards[:]
        for card in except_cards:
            rest_cards.remove(card)
        if len(rest_cards) == 2:
            return []
        else:
            rest_cards.sort()
            returs = len(rest_cards) - 2 # skip two cards
            return map(lambda (f, s): f, rest_cards[:returs])

    def _contain_face(self, cards, face):
        boxed_res = filter(lambda (f,_s): f == face, cards)
        return bool(boxed_res)

    def _longest_sequence(self, cards):
        sorted_cards = cards[:]
        sorted_cards.sort()
        current_seq, longest_seq = [sorted_cards[0]], [sorted_cards[0]]
        prev_f = sorted_cards[0][0]
        for f, s in sorted_cards[1:]:
            if f != prev_f + 1 and f != prev_f:
                if len(current_seq) > len(longest_seq):
                    longest_seq = current_seq
                current_seq = [(f,s)]
            elif f == prev_f:
                pass
            else:
                current_seq.append((f,s))
                if len(current_seq) > len(longest_seq):
                    longest_seq = current_seq
            prev_f = f
        return longest_seq

    def _same_suit_cards(self, cards):
        cards_by_suits = [[], [], [], []]
        for f, s in cards:
            cards_by_suits[s].append((f,s))
        sizes = map(len, cards_by_suits)
        size = max(sizes)
        max_suits = filter(lambda lst: len(lst) == size, cards_by_suits)
        # take first(any) suit, because if them > 1 len == 3(or 2 or 1)
        # and this is not the case we interest in
        max_suits[0].sort()
        return max_suits[0]
            

    def _is_same_suit(self, cards):
        first_suit = cards[0][1]
        b_seq = map(lambda (_f, s): s == first_suit)
        return all(b_seq)

    def _extract_cards(self, raw_cards):
        str_cards = raw_cards.split(" ")
        return [(self._face(c[0]), self._suit(c[1])) for c in str_cards]

    def _face(self, c):
        return self.FACES.index(c)

    def _suit(self, c):
        return self.SUITS.index(c)

    def hand_name(self):
        return self.HANDS[self.hand[0]]

    def rank(self):
        return self.HANDS_KEYS.index(self.hand[0])

    def top(self):
        return self.hand[1]

    def kickers(self):
        return self.hand[2]

def _best_hands(hands):
    best_ranks = _get_best_ranks(hands)
    if len(best_ranks) == 1:
        return [best_ranks[0].number]
    best_tops = _get_best_tops(best_ranks)
    if len(best_tops) == 1:
        return [best_tops[0].number]
    best_kickers = _get_best_kickers(best_tops)
    if len(best_kickers) == 1:
        return [best_kickers[0].number]
    else:
        return [k.number for k in best_kickers]


def _get_best_tops(hands):
    return _get_best_smth(hands, 'top')

def _get_best_kickers(hands):
    return _get_best_smth(hands, 'kickers')

def _get_best_smth(hands, smth):
    best_top = getattr(hands[0], smth)()
    best_hands = []
    for h in hands:
        h_top = getattr(h, smth)()
        if h_top == best_top:
            best_hands.append(h)
        elif h_top < best_top:
            best_hands = [h]
        else:
            pass
    return best_hands

def _get_best_ranks(hands):
    hand_ranks = []
    ranks = [h.rank() for h in hands if h]
    best_rank = min(ranks)
    best_ranks = [h for h in hands if h and h.rank() == best_rank]
    return best_ranks

def _create_hand(cards, num):
    size = len(cards.split(" "))
    if size != 7:
        return None
    else:
        return Hand(num, cards)

def _show_winner(num, winners):
    if len(winners) == 1 and [num] == winners:
        return "(Win)"
    elif num in winners:
        return "(Tie)"
    else:
        return ""

def who_winner(player_cards):
    hands = [_create_hand(cards, i) for i, cards in enumerate(player_cards)]
    winners = _best_hands(hands)
    for i, rcards in enumerate(player_cards):
        if hands[i]:
            print rcards.strip(), "|", hands[i].hand_name(), _show_winner(i, winners)
        else:
            print rcards.strip()

def main():
    raw_player_cards = [line for line in sys.stdin]
    who_winner(raw_player_cards)
    #r_cards = "5c 4c 3c 4c 2c Ac 2c"
    #hand = Hand(r_cards)
    #print r_cards
    #print hand.hand

if __name__ == "__main__":
    main()
