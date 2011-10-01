#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys

class Question(object):
    def __init__(self, question, yes, no):
        self.question = question
        self.yes, self.no = yes, no

    def ask(self, last_updater):
        result = ask_yn(self.question)
        if result:
            return self.yes.ask(self.yes_update)
        else:
            return self.no.ask(self.no_update)

    def yes_update(self, item):
        self.yes = item

    def no_update(self, item):
        self.no = item


class Answer(object):
    def __init__(self, text):
        self.text = text

    def ask(self, last_updater):
        return (last_updater, self, ask_yn("Is it %s" % self.text))


def main():
    first_question = Answer("an elephant")
    continue_game = True
    while continue_game:
        continue_game, first_question = start_new_game(first_question)

def start_new_game(first_question):
    print "Think of an animal..."
    last_updater, last_answer, i_win = first_question.ask(None)
    if i_win:
        print "I win. Pretty smart, aren't I?"
    else:
        print "You win. Help me learn from my mistake before you go..."
        new_question = learn_new_question(last_answer, last_updater, first_question)
        first_question = update_question_list(first_question, last_updater, new_question)
    return (ask_yn("Play again?"), first_question)

def learn_new_question(last_answer, last_updater, first_question):
    answer = raw_input("What animal were you thinking of?\n")
    wrong_answer = last_answer.text
    question = raw_input("Give me a question to distinguish %s from %s.\n" % (answer, wrong_answer))
    yn_answer = ask_yn("For %s, what is the answer to your questions?" % answer)
    if yn_answer:
        new_question = Question(question, Answer(answer), last_answer)
    else:
        new_question = Question(question, last_answer, Answer(answer))
    return new_question

def update_question_list(first_question, last_updater, new_question):
    if last_updater:
        last_updater(new_question)
    else:
        first_question = new_question
    return first_question

def ask_yn(question):
    answer = raw_input("%s (y or n)\n" % question)
    return answer == 'y' or answer == 'Y'

if __name__ == '__main__':
    main()
