#!/usr/bin/env python 
# -*- coding: utf-8 -*-

class Line(object):
    def __init__(self, chunk, max_x, max_y):
        self.dots = set()
        self.max_x, self.max_y = max_x, max_y
        self.dots.add(chunk[0])
        self.dots.add(chunk[1])
        self.chunks.add(chunk)

    def _has_chunk(self, chunk):
        if chunk in self.chunks:
            return True

    def try_append(self, chunk):
        if self._has_chunk(chunk):
            return True
        (xy1, xy2) = chunk
        if xy1 in self.dots:
            return _try_append(xy2, chunk)
        elif xy2 in self.dots:
            return _try_append(xy1, chunk)
        else:
            return False
            
    def _try_append(self, xy, chunk):
        self.dots.add(xy)
        if self._check_line_correctness():
            self.chunks.add(chunk)
            return True
        else:
            self.dots.remove(xy)
            return False

    # 1) line should not touch more then one border point
    # 2) line should not have any loops
    def self._check_line_correctness(self):
        return self._check_not_touch_more_then_one_border_point() and self._check_not_contain_any_loops()

    def _check_not_touch_more_then_one_border_point(self):
        touch_border_num = 0
        for (x,y) in self.dots:
            if x == 0 or x == self.max_x or y == 0 or y == self.max_y:
                touch_border_num += 1
        return touch_border_num <= 1

    def _check_not_contain_any_loops(self):
        pass

            


class Maze(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.chunks, self.lines = set(), []

    def generate():
        self._generate_chunks()
        self._bind_dangling_lines()

    def output(self):
        pass

    def _generate_chunks(self):
        for x, y in inner_dots():
            while True:
                new_chunks = self._random_chunks(x, y)
                attached = 0
                for chunk in new_chunks:
                    if self._attach_chunk_to_line(chunk):
                        attached += 1
                if attached:
                    break

    def _attach_chunk_to_line(self, chunk):
        for line in self.lines:
            if line.try_append(chunk):
                return True
        # create new line
        self.lines.append(Line(chunk, self.x, self.y))
        return True

    def _bind_dangling_lines(self):
        pass

    def _random_chunks(self, x, y):
        mask = random.randint(1, 14)
        chunks = []
        if mask & 1:
            chunk = ((x, y), (x+1, y))
            chunks.append(chunk)
        if mask & 2:
            chunk = ((x, y-1), (x, y))
            chunks.append(chunk)
        if mask & 4:
            chunk = ((x-1, y), (x, y))
            chunks.append(chunk)
        if mask & 8:
            chunk = ((x, y), (x, y+1))
            chunks.append(chunk)
        return chunks

    def inner_dots(self):
        for x in xrange(1, self.x-1):
            for y in xrange(1, self.y-1):
                yield (x, y)

def main():
    Maze(2, 2).generate().output()

if __name__ == "__main__":
    main()

