#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys

def encrypt(text):
    AZ_text = _discard_uppercase_and_split(text)
    keystream = _keystream(len(AZ_text))
    num_AZ_text = _convert_string_to_digits(AZ_text)
    num_keystream = _convert_string_to_digits(keystream)
    combined_streams = _combine_two_sequence(num_AZ_text, num_keystream)
    encrypted_sequence = _convert_digits_to_string(combined_streams)
    return encrypted_sequence

def decrypt(raw_text):
    text = _discard_uppercase_and_split(raw_text)
    keystream = _keystream(len(text))
    num_text = _convert_string_to_digits(text)
    num_keystream = _convert_string_to_digits(keystream)
    sub_streams = _substract_two_sequence(num_text, num_keystream)
    decrypted_sequence = _convert_digits_to_string(sub_streams)
    return decrypted_sequence

def _substract_two_sequence(first, second):
    raw = [a - b for a, b in zip(first, second)]
    return map(lambda n: n + 26 if n < 1 else n, raw)

def _combine_two_sequence(first, second):
    raw = [a + b for a, b in zip(first, second)]
    return map(lambda n: n - 26 if n > 26 else n, raw)

def _convert_digits_to_string(digits):
    return "".join(map(lambda c: chr(c + ord('A') - 1), digits))

def _convert_string_to_digits(string):
    return map(lambda c: ord(c) - ord('A') + 1, string)

class Deck(object):
    def __init__(self):
        self.deck = self._key_the_deck()
        self._update_jocker_state()

    def _key_the_deck(self):
        deck = list(xrange(1, 53))
        deck.append('A')
        deck.append('B')
        return deck

    def generate_letter(self):
        self._move_a_jocker_down_one_cards()
        self._move_b_jocker_down_two_cards()
        self._do_triple_cut()
        self._do_count_cut()
        return self._find_output_letter()

    def _move_a_jocker_down_one_cards(self):
        self._move_jocker_down_one_cards("a_jocker")

    def _move_b_jocker_down_two_cards(self):
        self._move_jocker_down_one_cards("b_jocker")
        self._move_jocker_down_one_cards("b_jocker")

    def _move_jocker_down_one_cards(self, name):
        jocker = getattr(self, name)
        if jocker != 53:
            another = jocker + 1
            self._swap(jocker, another)
        else:
            first = self.deck[0]
            tail_but_last = self.deck[1:-1] # but first and last(jocker)
            self.deck = [first, self.deck[-1]] + tail_but_last
        self._update_jocker_state()

    def _swap(self, first, second):
        value1, value2 = self.deck[first], self.deck[second]
        self.deck[first], self.deck[second] = value2, value1

    def _do_triple_cut(self):
        if self.a_jocker < self.b_jocker:
            top_jocker, bottom_jocker = self.a_jocker, self.b_jocker
        else:
            top_jocker, bottom_jocker = self.b_jocker, self.a_jocker
        head_chunk = self.deck[:top_jocker]
        bottom_chunk = self.deck[(bottom_jocker + 1):]
        middle_chunk = self.deck[top_jocker:(bottom_jocker + 1)]
        self.deck = bottom_chunk + middle_chunk + head_chunk
        self._update_jocker_state()

    def _update_jocker_state(self):
        self.a_jocker, self.b_jocker = self._find_jocker('A'), self._find_jocker('B')

    def _do_count_cut(self):
        bottom_card = self.deck[-1]
        if bottom_card in ['A', 'B']:
            return
        top_slice = self.deck[:bottom_card]
        up_to_bottom = self.deck[bottom_card:-1]
        self.deck = up_to_bottom + top_slice + [bottom_card]
        self._update_jocker_state()

    def _value(self, value):
        if value in ['A', 'B']:
            return 53
        else:
            return value

    def _letter(self, value):
        num = value if value <= 26 else value - 26
        return chr(num + ord('A') - 1)

    def _find_output_letter(self):
        top_card = self.deck[0]
        letter_card = self.deck[self._value(top_card)]
        if letter_card in ['A', 'B']:
            return ""
        else:
            return self._letter(letter_card)


    def _find_jocker(self, letter):
        for i, c in enumerate(self.deck):
            if c == letter:
                return i

                

def _keystream(size):
    # stub
    #return "DWJXHYRFDGTMSHPUURXJ"
    deck = Deck()
    result = ""
    while len(result) < size:
        result += deck.generate_letter()
    return result

def _discard_uppercase_and_split(text):
    upper = [c.upper() for c in text if c.isalpha()]
    splitted = map(lambda x: "".join(upper[x:x+5]), list(xrange(len(upper)))[::5])
    if len(splitted[-1]) != 5:
        splitted[-1] = splitted[-1] + 'X' * (5 - len(splitted[-1]))
    return "".join(splitted)

def main():
    if sys.argv[1] == "-d":
        print decrypt(sys.argv[2])
    elif sys.argv[1] == "-e":
        print encrypt(sys.argv[2])
    else:
        print encrypt(sys.argv[1])

    #print _keystream(20)

if __name__ == "__main__":
    main()
