#!/usr/bin/env python3

import sys

def adjacent(c0, c1):
    return abs(c0[0] - c1[0]) < 2 and abs(c0[1] - c1[1]) < 2

def distance(c0, c1):
    """
    Manhattan distance between two coordinates
    """
    return abs(c0[0] - c1[0]) + abs(c0[1] - c1[1])

deltas = {   # (x, y)
    'U': (0, 1),
    'D': (0, -1),
    'R': (1, 0),
    'L': (-1, 0)
}

class Simulator:
    def __init__(self, nknots):
        self.nknots = nknots
        self.knots = [(0,0)] * nknots
        self.total_steps = 0
        self.trail = {(0,0)}

    def printCurrent(self):
        kmin_x, kmax_x = min(c[0] for c in self.knots), max(c[0] for c in self.knots)
        kmin_y, kmax_y = min(c[1] for c in self.knots), max(c[1] for c in self.knots)
        max_x, max_y = max(0, kmax_x), max(0, kmax_y)
        min_x, min_y = min(0, kmin_x), min(0, kmin_y)
        field = [(['.'] * (max_x - min_x + 1)) for k in range((max_y - min_y + 1))]
        def write_on(x, y, c):
            field[y - min_y][x - min_x] = c
        write_on(0, 0, 's')
        names = ['H'] + list(str(k) for k in range(1, self.nknots))
        for knot, name in reversed(list(zip(self.knots, names))):
            write_on(knot[0], knot[1], name)
        print('\n'.join(''.join(l) for l in reversed(field)))

    def move(self, to_dir, steps):
        if steps == 0: # We could assume this is true, but just in case...
            return ()

        hdx, hdy = deltas[to_dir]

        for k in range(steps):
            head = self.knots[0]
            prev = (head[0] + hdx, head[1] + hdy)
            self.knots[0] = prev
            for i, knot in enumerate(self.knots[1:], 1):
                d = distance(knot, prev)
                dfx, dfy = prev[0] - knot[0], prev[1] - knot[1]
                if distance(knot, prev) > 1 and (abs(dfx) > 1 or abs(dfy) > 1):
                    dx, dy = (dfx // abs(dfx) if dfx else 0), (dfy // abs(dfy) if dfy else 0)
                    prev = self.knots[i] = (knot[0] + dx, knot[1] + dy)
                else:
                    break
            else:
                self.trail.add(prev)

    def get_number_tail_positions(self):
        return len(self.trail)

def read_input(stream):
    for line in stream:
        direction, steps = line.strip().split()
        yield direction, int(steps)

def main(data, prn=True, debug=False):
    sim1 = Simulator(2)
    sim2 = Simulator(10)
    if debug:
        print("== Initial Case ==")
        sim2.printCurrent()
    for direction, steps in data:
        sim1.move(direction, steps)
        sim2.move(direction, steps)
        if debug:
            print(f"== {direction} {steps} ==")
            sim2.printCurrent()

    if prn:
        print("Number of unique positions visited by the tail")
        print(" 2 Knots: ", sim1.get_number_tail_positions())
        print("10 Knots: ", sim2.get_number_tail_positions())

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
