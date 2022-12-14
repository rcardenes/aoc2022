#!/usr/bin/env python3
import sys
from pprint import pprint
from copy import deepcopy

class Map:
    def __init__(self, left, right, bottom):
        self.left = left
        self.width = right - left + 1
        self.height = bottom + 3
        self.rep = ['.'] * (self.width * (self.height - 1))
        self.rep.extend(['#'] * self.width)

    def add_line(self, a, b):
        ax, ay = a
        bx, by = b

        xrng = tuple(range(min(ax, bx), max(ax, bx)+1))
        yrng = tuple(range(min(ay, by), max(ay, by)+1))
        lx, ly = len(xrng), len(yrng)
        xrng = xrng * ly
        yrng = yrng * lx

        for x, y in zip(xrng, yrng):
            self.rep[(self.width * y) + (x - self.left)] = '#'

    def expand(self, to_left):
        width = self.width
        newrep = []
        for y in range(self.height - 1):
            offset = y * width
            if to_left:
                newrep.extend(['.'] + self.rep[offset:offset + width])
            else:
                newrep.extend(self.rep[offset:offset + width] + ['.'])
        newrep.extend(['#']*(width + 1))

        self.rep = newrep
        if to_left:
            self.left = self.left - 1
        self.width = self.width + 1

        return (self.width - 1), self.width

    def simulate(self, void=False):
        fn = self.drop if void else self.bounded_drop

        step = 0
        while fn():
            step += 1
        return step if void else (step + 1)

    def drop(self):
        """
        Simulates a grain of sand dropping, assuming an endless bottom.

        Returns `True` if the grain comes to rest within bounds
        """

        width = self.width
        bottom, right = self.height - 3, self.width - 1

        x, y = (500 - self.left), 0
        while True:
            nexty = y + 1
            leftof = x - 1
            rightof = x + 1

            offset = nexty * width + x
            if nexty > bottom:
                break
            elif self.rep[offset] == '.':
                y += 1
                continue

            offset = nexty * width + leftof
            if leftof < 0:
                break
            elif self.rep[offset] == '.':
                x -= 1
                y += 1
                continue

            offset = nexty * width + rightof
            if rightof > right:
                break
            elif self.rep[offset] == '.':
                x += 1
                y += 1
                continue

            self.rep[y * width + x] = 'o'
            return True

        return False

    def bounded_drop(self):
        """
        Simulates a grain of sand dropping, assuming a flat bottom.

        Returns `True` if the grain didn't block the entrance
        """

        left, width = self.left, self.width
        bottom, right = self.height - 1, self.width - 1

        x, y = (500 - left), 0
        steps = 0
        while True:
            nexty = y + 1
            leftof = x - 1
            rightof = x + 1
            steps += 1

            offset = nexty * width + x
            if self.rep[offset] == '.':
                y += 1
                continue

            if leftof < 0:
                right, width = self.expand(to_left=True)
                x = 1
                continue

            offset = nexty * width + leftof
            if self.rep[offset] == '.':
                x -= 1
                y += 1
                continue

            if rightof > right:
                right, width = self.expand(to_left=False)
                continue

            offset = nexty * width + rightof
            if self.rep[offset] == '.':
                x += 1
                y += 1
                continue

            self.rep[y * width + x] = 'o'
            return steps > 1

    def print(self):
        for y in range(self.height):
            offset = y * self.width
            print(''.join(self.rep[offset:offset + self.width]))

def main(data):
    caveMap = data

    p1 = deepcopy(caveMap)
    units = p1.simulate(void=True)
    print("Units of sand before it starts pouring:", units)

    p2 = deepcopy(caveMap)
    units = p2.simulate(void=False)
    print("Units of sand before it gets blocked:", units)

def read_input(stream):
    paths = []
    bounding_box = [None, None, None]
    def update_bounding_box(x, y):
        left, bottom, right = bounding_box
        if bottom is None or bottom < y:
            bounding_box[1] = y
        if left is None or left > x:
            bounding_box[0] = x
        if right is None or right < x:
            bounding_box[2] = x
    for line in stream:
        vertices = []
        for vt in line.strip().split(' -> '):
            x, y = tuple(int(k) for k in vt.split(','))
            vertices.append((x, y))
            update_bounding_box(x, y)
        paths.append(vertices)

    caveMap = Map(bounding_box[0], bounding_box[2], bounding_box[1])
    for path in paths:
        for a, b in zip(path[:-1], path[1:]):
            caveMap.add_line(a, b)

    return caveMap

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
