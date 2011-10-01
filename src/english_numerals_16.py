#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys

NUMBERS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
}

ORDERS = ["", "thousand", "million", "billion"]

def pronounce(digit):
    direct_digit = _get_direct_digit(digit)
    if direct_digit:
        return direct_digit
    full_digit = []
    for order, num in _triplets(digit):
        result = _spell_triplet(order, num)
        if result:
            full_digit.append(result)
    return " ".join(full_digit)

def _spell_triplet(order, num):
    direct_digit = _get_direct_digit(num)
    if num and direct_digit:
        return _append_order(direct_digit, order)
    if not num:
        return ""
    str_num = str(num)
    spelled_digit = ""
    if len(str_num) == 2:
        spelled_digit = _spell_two_digit(str_num)
        return _append_order(spelled_digit, order)
    elif len(str_num) == 3:
        spelled_digit = _spell_three_digit(str_num)
        return _append_order(spelled_digit, order)

def _spell_two_digit(dirty_str_num):
    # remove leading zero if exists
    str_num = str(int(dirty_str_num))
    if str_num == "0":
        return ""
    if len(str_num) == 1:
        return NUMBERS[int(str_num)]
    high = int(str_num[0]) * 10
    low = int(str_num[1])
    return NUMBERS[high] + "-" + NUMBERS[low]

def _spell_three_digit(str_num):
    high = int(str_num[0])
    low = _spell_two_digit(str_num[1:])
    return NUMBERS[high] + " hundread " + low

def _append_order(digit, order):
    if order:
        return digit + " " + order
    else:
        return digit

def _triplets(digit):
    string = str(digit)
    high_order = ((len(string) - 1) / 3)
    high_len = (len(string) % 3) or 3
    high_digit = int(string[0:high_len])
    yield ORDERS[high_order], high_digit
    aligned_string = string[high_len:]
    for order, i in zip(reversed(xrange(high_order)), xrange(high_order)):
        shift = i * 3
        yield ORDERS[order], int(aligned_string[shift:shift + 3])

def _get_direct_digit(digit):
    if digit in NUMBERS:
        return NUMBERS[digit]
    else:
        return None

def main():
    print pronounce(17)
    print pronounce(90)
    print pronounce(10000234)

if __name__ == "__main__":
    main()
