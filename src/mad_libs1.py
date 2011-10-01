#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import random
import re

sentences = [
    #"I had a ((an adjective)) sandwich for lunch today. It dripped all over my ((a body part)) and ((a noun))",
    "Our favourite language is ((gem:a gemstone)). We think ((gem)) is better than ((gem2:a gemstone)). And i love this ((gem)) much more than ((gem2))"
        ]

def select_random_string(sentences):
    return random.choice(sentences)

def ask_questins(string):
    questions, placeholders = get_all_questions(string)
    answers = []
    for q in questions:
        answer = raw_input(q).strip()
        answers.append(answer)
    return (answers, placeholders)

def get_all_questions(string):
    raw_questions = re.findall(r'(?:\(\()([^)]+)(?:\)\))', string)
    keywords = {}
    questions = []
    placeholders = []
    for i, l in enumerate(raw_questions):
        seq = l.split(":")
        if len(seq) > 1:
            questions.append(seq[1])
            keywords[seq[0]] = ((len(questions)-1), seq[1])
            placeholders.append(len(questions)-1)
        else:
            if l in keywords:
                prev_i, _quest = keywords[l]
                placeholders.append(prev_i)
            else:
                questions.append(l)
                placeholders.append(len(questions)-1)
    return (questions, placeholders)

def show_result(string, answers, placeholders):
    parts = re.split(r'\(\([^)]+\)\)', string)
    last = len(parts) - 1
    print "result"
    print placeholders
    print answers
    print parts
    for i, p in enumerate(parts):
        if i != last:
            print p, answers[placeholders[i]],
        else:
            print p,

def main():
    string = select_random_string(sentences)
    print string
    (answers, placeholders) = ask_questins(string)
    show_result(string, answers, placeholders)

if __name__ == "__main__":
    main()
