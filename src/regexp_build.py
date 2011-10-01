#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import re

class Range:
    def __init__(self, min_v, max_v):
        self.max_v = max_v
        self.min_v = min_v
        self.iter  = xrange(min_v, max_v)

    def max(self):
        return max_v

    def min(self):
        return min_v

    def __iter__(self):
        return iter(self.iter)

    def build_re(self):
        return self.build_regex(str(self.min_v), str(self.max_v))

    def build_regex(self, min_v, max_v):
        print "Range: %s-%s" % (min_v, max_v)
        ranges = self.split_by_degree(min_v, max_v)
        regexes = [self.regex_for_range(minv, maxv) for minv, maxv in ranges]
        return regexes

    def regex_for_range(self, min_v, max_v):
        one_char_regex = self.get_one_char_regex(min_v, max_v)
        if one_char_regex:
            return one_char_regex
        result = self.find_common_prefix(min_v, max_v)
        prefix = ""
        if result:
            prefix, rest_min, rest_max = result
        else:
            rest_min, rest_max = min_v, max_v
        one_char_regex = self.get_one_char_regex(rest_min, rest_max)
        if one_char_regex:
            return self.combine_regex(prefix, (one_char_regex,))
        low, middle, high = self.regex_for_same_degree(rest_min, rest_max)
        return self.combine_regex(prefix, (low, middle, high))

    def get_one_char_regex(self, min_v, max_v):
        if min_v == max_v:
            return min_v
        if len(min_v) == 1:
            return self.build_bracket_range_regex(min_v, max_v)
        return None

    def regex_for_same_degree(self, min_v, max_v):
        low = self.build_low_regex(min_v)
        high = None
        middle = self.build_middle_regex(min_v, max_v)
        high = self.build_high_regex(max_v)
        return low, middle, high

    def combine_regex(self, prefix, regexes):
        not_none_regexes = filter(lambda x: x is not None, regexes)
        inner_regex = "|".join(not_none_regexes)
        if prefix:
            print "HEEE"
            return "%s%s" % (prefix, self.regex_put_in_braces(inner_regex))
        else:
            return inner_regex

    def regex_put_in_braces(self, regex):
        if regex == r"\d" or regex == r"\\d" or len(regex) == 1:
            return regex
        else:
            return "(%s)" % regex

    def build_low_regex(self, min_v):
        if self.can_be_added_to_middle(min_v):
            return None
        max_v = self.round_till_next_number(min_v)
        print "low:", min_v, max_v
        res = self.regex_for_range(min_v, max_v)
        print "low res:", res
        return res

    def can_be_added_to_middle(self, number):
        zero_num = "0" * (len(number) - 1)
        return number[1:] == zero_num

    def build_high_regex(self, max_v):
        min_v = self.round_down(max_v)
        print "high:", min_v, max_v
        res = self.regex_for_range(min_v, max_v)
        print "high res:", res
        return res

    def round_down(self, number):
        first_digit = self.first_digit(number)
        num_len = len(str(number))
        s_number = "0" * num_len
        return s_number.replace("0", str(first_digit), 1)

    def round_till_next_number(self, number):
        first_digit = self.first_digit(number)
        num_len = len(str(number))
        s_number = "9" * num_len
        return s_number.replace("9", str(first_digit), 1)

    def build_middle_regex(self, uncut_min_v, uncut_max_v):
        print uncut_min_v, uncut_max_v
        min_v, max_v = self.find_middle_range(uncut_min_v, uncut_max_v)
        if not min_v:
            return None
        first_min_digit, first_max_digit = map(self.first_digit, [min_v, max_v])
        rest_digits = r'\d' * (len(min_v) - 1)
        if first_min_digit == first_max_digit:
            return "%s%s" % (first_min_digit, rest_digits)

        return "%s%s" % (self.build_bracket_range_regex(first_min_digit, first_max_digit), rest_digits)

    def build_bracket_range_regex(self, first, second):
        if str(first) == "0" and str(second) == "9":
            return r'\d'
        else:
            return "[%s-%s]" % (first, second)

    def find_middle_range(self, uncut_min, uncut_max):
        first_min_digit, first_max_digit = map(self.first_digit, [uncut_min, uncut_max])
        if self.can_be_added_to_middle(uncut_min):
            diff = first_max_digit - first_min_digit + 1
        else:
            diff = first_max_digit - first_min_digit
        print diff
        if diff > 1:
            return (self.round_up(uncut_min), self.round_till(uncut_max))
        else:
            return None, None

    def round_up(self, number):
        if self.can_be_added_to_middle(number):
            return number
        first_digit = self.first_digit(number)
        num_len = len(str(number))
        s_number = "0" * num_len
        return s_number.replace("0", str(first_digit + 1), 1)

    def round_till(self, number):
        first_digit = self.first_digit(number)
        num_len = len(str(number))
        s_number = "9" * num_len
        return s_number.replace("9", str(first_digit - 1), 1)

    def first_digit(self, number):
        return int(str(number)[0])

    def find_common_prefix(self, min_v, max_v):
        prefix = ""
        for i, c in enumerate(min_v):
            if c == max_v[i]:
                prefix += c
            else:
                break
        if prefix:
            rest_min = min_v[len(prefix):]
            rest_max = max_v[len(prefix):]
            return (prefix, rest_min, rest_max)
        else:
            return None

    def split_by_degree(self, min_v, max_v):
        current_min = min_v
        ranges = []
        for i in xrange(len(str(min_v)), len(str(max_v))+1):
            current_max = max_v if i == len(str(max_v)) else 10 ** i - 1
            current_min = min_v if i == len(str(min_v)) else 10 ** (i - 1)
            ranges.append((current_min, current_max))
        return ranges

def main():
    #r = Range(3, 6).build_re()
    #print r
    r = Range(30293, 30536).build_re()
    print r
    r = Range(30293, 30436).build_re()
    print r
    #assert(re.match(r, "12"))
    #assert(re.match(r, "99"))
    #assert(not re.match(r, "0"))
    print "All ok"

if __name__ == "__main__":
    main()
