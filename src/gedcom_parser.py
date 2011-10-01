#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from __future__ import with_statement

# 0 @I1@ INDI
# 1 NAME Jamis Gordon /Buck/
# 2 SURN Buck
# 2 GIVN Jamis Gordon
# 1 SEX M
#
# <gedcom>
#   <indi id="@I1">
#     <name>
#       Jamis Gordon /Buck/
#       <surn>Buck</surn>
#       <givn>Jamis Gordon</givn>
#     </name>
#     <sex>M</sex>
#   </indi>
# </gedcom>

import sys

def main():
    output_tree_as_xml(sys.argv[1])

def output_tree_as_xml(filename):
    print "<gedcom>"
    stack = [(-1, "</gedcom>")]
    for (level, next_level), (kind, name), data in parser(filename):
        print upper_ctags(stack, level)
        if next_level <= level:
            print tag(level, kind, name, data), close_tag(level, kind, name, data)[1]
        else:
            print tag(level, kind, name, data)
            stack.append(close_tag(level, kind, name, data))
    for lvl, ctag in reversed(stack):
        print ctag

def upper_ctags(stack, new_level):
    utags = ""
    for lvl, ctag in reversed(stack):
        if new_level > lvl:
            return utags
        else:
            stack.pop()
            utags += "\n" + ctag
    return utags

            

def tag(level, kind, name, data):
    if 'tag' == kind:
        return "%s<%s>%s" % (indent(level), name, data)
    else:
        return '%s<%s id="@%s">' % (indent(level), data, name)

def close_tag(level, kind, name, data):
    if 'tag' == kind:
        tag_name = name
    else:
        tag_name = data
    return (level, "%s</%s>" % (indent(level), tag_name))

def indent(level):
    return ' ' * (level * 2 + 2)

def parser(filename):
    with open(filename) as f:
        fiter = iter(f)
        last_line = None
        for next_line in fiter:
            if last_line is None:
                current_line = next_line
                next_line = fiter.next()
            else:
                current_line = last_line
            last_line = next_line
            next_level = extract_level(next_line)
            level, tag_or_id, data = extract_data(current_line)
            yield (level, next_level), tag_or_id, data

def extract_level(line):
    level, tag_or_id, data = extract_data(line)
    return level

def extract_data(line):
    parts = line.split(" ", 2)
    if len(parts) == 3:
        level_s, tag_or_id, data = parts
    else:
        level_s, tag_or_id = parts
        data = ""
    return int(level_s), tag_id(tag_or_id), data.strip()

def tag_id(text):
    if text.startswith("@") and text.endswith("@"):
        return ('id', text[1:-1])
    else:
        return ('tag', text)

def read_content(filename):
    f = open(filename)
    text = f.read()
    f.close
    return text

if __name__ == '__main__':
    main()
