#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys


number_to_phone = {
        2: ['a', 'b', 'c'],
        3: ['d', 'e', 'f'],
        4: ['g', 'h', 'i'],
        5: ['j', 'k', 'l'],
        6: ['m', 'n', 'o'],
        7: ['p', 'q', 'r', 's'],
        8: ['t', 'u', 'v'],
        9: ['w', 'x', 'y', 'z']
        }

dictionary_file = "words.lst"

def convert_with_text(dirty_phone):
    variants = convert(dirty_phone)
    return "> " + "\n> ".join(variants)

def convert(dirty_phone):
    phone = _leave_numbers(dirty_phone)
    number_combinations = _generate_combinations(phone)

    dictionary = _read_dict()
    all_branches = _generate_branches_for_combo(number_combinations, dictionary)
    mnemos = _generate_mnemos(all_branches)
    return mnemos

def _generate_mnemos(all_branches):
    answers = []
    for branch in all_branches:
        answers.extend(_gen_mnemos(branch))
    return map(_pretty_print, answers)

def _pretty_print(answer):
    return "-".join(answer)

def _gen_mnemos(branch, all_mnemos=None, seq=None):
    if len(branch) == 0:
        all_mnemos.append(seq[:])
        return
    if all_mnemos is None:
        all_mnemos = []
    for leaf in branch[0]:
        if seq is None:
            seq = []
        nseq = seq[:]
        nseq.append(leaf)
        _gen_mnemos(branch[1:], all_mnemos, nseq)
    return all_mnemos


def _generate_branches_for_combo(number_combinations, dictionary):
    all_branches = []
    for combo in number_combinations:
        branch = []
        for num in combo:
            words = _try_to_generate_words(num, dictionary)
            if words:
                branch.append(words)
            else:
                break
        else:
            all_branches.append(branch)
    return all_branches

def _generate_combinations(phone):
    dirty_combinations = _do_generate_combinations(phone, len(phone))
    number_combinations = _remove_incorrect_combinations(dirty_combinations)
    return number_combinations

def _remove_incorrect_combinations(dirty_combinations):
    return filter(_is_correct_combo, dirty_combinations)

def _is_correct_combo(combo):
    prev_len = 0
    for s in combo:
        if prev_len == len(s) and prev_len == 1:
            return False
        prev_len = len(s)
    return True

def _do_generate_combinations(phone, max_len, branch="root", level=0):
    #print "Start", branch, level
    combinations = []
    for width in xrange(max_len, 0, -1):
        if width > len(phone):
            #print "PPP:", phone
            continue
        for pos in xrange(len(phone) - width + 1):
            #print "Prev:", phone[:pos], width-1
            prev_str = phone[:pos]
            prev_combinations = _do_generate_combinations(phone[:pos], width-1, "prev", level+1)
            if prev_str and not prev_combinations:
                continue
            current_combo = phone[pos:(pos + width)]
            #print "Curr:", current_combo
            #print "Next:", phone[(pos + width):]
            next_combinations = _do_generate_combinations(phone[(pos + width):], width, "next", level+1)
            combs = _combine_triplet(prev_combinations, current_combo, next_combinations)
            #print "LPCN:", pos, width, prev_combinations, current_combo, next_combinations
            #print combs
            combinations.extend(combs)
            #if width < 4 and len(phone) == 7:
                #return combinations
    #print "End", branch, level
    return combinations

def _combine_triplet(prev_combinations, middle, next_combinations):
    if prev_combinations == []:
        prev_combinations = [[]]
    if next_combinations == []:
        next_combinations = [[]]
    res = [_combine_three(prev, middle, next)
            for prev in prev_combinations for next in next_combinations]
    return res

def _combine_three(prev, middle, next):
    combo = prev[:]
    combo.append(middle)
    combo.extend(next)
    return combo

def _select_proper_words(words_for_phone, dictionary):
    proper_words = []
    for w in words_for_phone:
        if w in dictionary:
            proper_words.append(w)
    return proper_words

def _try_to_generate_words(phone, dictionary):
    if len(phone) == 1:
        return [phone]
    else:
        any_words = _generate_words(phone)
        proper_words = _select_proper_words(any_words, dictionary)
        return proper_words


def _generate_words(phone, cur_str=""):
    if phone == "":
        return cur_str
    d = phone[0]
    letters = number_to_phone[int(d)]
    result = []
    for l in letters:
        res = _generate_words(phone[1:], cur_str + l)
        if isinstance(res, list):
            result.extend(res)
        else:
            result.append(res)
    return result



def _leave_numbers(phone):
    num_list = map(str, xrange(10))
    lphone = []
    for c in phone:
        if c in num_list:
            lphone.append(c)
    return "".join(lphone)
            

def _read_dict():
    dictionary = {}
    with open(dictionary_file) as f:
        for dirty_word in f:
            word = dirty_word.strip()
            if "'" in word:
                continue
            dictionary[word] = True
    return dictionary


def main():
    #res = _generate_combinations("2345678")
    #l = [[['tpd', 'trf', 'urf', 'use'], ['quaw', 'ruby']] ]
    #res = _generate_mnemos(l)
    #print res

    for line in sys.stdin:
        if not line:
            return
        print convert_with_text(line)
    #res = convert("873.7829")
    #print res
    #print len(res)
    #print convert("774.3277")

if __name__ == "__main__":
    main()
