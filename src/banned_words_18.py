#!/usr/bin/env python 
# -*- coding: utf-8 -*-

DICTIONARY = [
    "foo", "bar", "size", "six", "seven", "test", "cool", "juice",
    "fruit", "orange", "frog", "nail", "hand", "arm", "costume", "ball"
]

class LanguageFilter(object):
    def __init__(self, *banned_words):
        print banned_words
        self.banned_words = list(banned_words)
        self.banned_words.sort()
        self.clean_calls = 0

    def is_clean(self, words):
        self.clean_calls += 1
        for word in self.banned_words:
            if word in words:
                return False 
        return True

    def verify(self, *out_suspect_words):
        suspect_words = list(out_suspect_words)
        suspect_words.sort()
        return suspect_words == self.banned_words

class BinarySearch(object):
    def __init__(self, filter_, dict_):
        self.filter, self.dict = filter_, dict_

    def find(self):
        banned_words = self._find(self.dict)
        print banned_words
        if self.filter.verify(*banned_words):
            print "Ok", self.filter.clean_calls
        else:
            print "Bad" 

    def _find(self, words):
        banned_words = []
        middle = len(words) / 2
        fpart, spart = words[:middle], words[middle:]
        self._check_and_add(banned_words, fpart)
        self._check_and_add(banned_words, spart)
        return banned_words

    def _check_and_add(self, banned_words, words):
        if len(words) == 0:
            return
        if not self._is_clean(words):
            print "Here"
            if len(words) == 1:
                print "Here2"
                banned_words.extend(words)
            else:
                print "Here3"
                banned_words.extend(self._find(words))

    def _is_clean(self, words):
        return self.filter.is_clean(words)
        



def main():
    filter_ = LanguageFilter("hand")
    strategy = BinarySearch(filter_, DICTIONARY)
    strategy.find()

if __name__ == "__main__":
    main()
