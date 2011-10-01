#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import re

def ask_yn(question):
    answer = raw_input("%s (y or n)\n" % question)
    return answer == 'y' or answer == 'Y'

def ask(question, kind, **args):
    while True:
        answer = raw_input("%s \n" % question)
        try:
            result = _extract(answer, kind, args)
            return result
        except ValueError, ex:
            if ex.args:
                print ex.args[0]
            else:
                print "Incorrect value. Try again."

def _extract(answer, kind, args):
    if kind == int:
        return _extract_integer(answer, **args)
    elif kind == str:
        return _extract_string(answer, **args)
    else:
        raise NotImplementedError

def _extract_integer(string, within=None):
    try:
        result = int(string)
    except ValueError:
        raise ValueError("Incorrect number")
    if not within:
        return result
    low, high = within
    if result >= low and result <= high:
        return result
    else:
        raise ValueError("Incorrect value, number should be in range %s..%s" % (low, high))

def _extract_string(string, validate=None):
    if not validate:
        return string
    if re.match(validate, string):
        return string
    else:
        raise ValueError

def main():
    result = ask("Enter your age", int, within=(10, 120))
    print "Answer: %s" % result
    result = ask("Enter your name", str, validate=r"[a-zA-Z]{2,}")
    print "Answer: %s" % result


if __name__ == "__main__":
    main()
