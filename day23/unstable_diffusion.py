#!/usr/bin/env python3
import sys
from collections import defaultdict
from pprint import pprint

class DiffusionEngine:
    def __init__(self):
        self.order = ('N', 'S', 'W', 'E')

    def __call__(self, current_positions, dimensions):
        rows, cols = dimensions
        decisions = defaultdict(set)

        new_positions = set()
        for (erow, ecol) in current_positions:
            surrounding_coords = (
                    (erow-1, ecol-1), (erow-1, ecol), (erow-1, ecol+1),
                    (erow, ecol-1), (erow, ecol+1),
                    (erow+1, ecol-1), (erow+1, ecol), (erow+1, ecol+1)
                    )
            if set(surrounding_coords) & current_positions:
                for d in self.order:
                    if d == 'N' and not current_positions & set(surrounding_coords[:3]):
                        decisions[(erow - 1, ecol)].add((erow, ecol))
                        break
                    elif d == 'S' and not current_positions & set(surrounding_coords[-3:]):
                        decisions[(erow + 1, ecol)].add((erow, ecol))
                        break
                    elif d == 'W' and not current_positions & set((surrounding_coords[0], surrounding_coords[3],surrounding_coords[5])):
                        decisions[(erow, ecol - 1)].add((erow, ecol))
                        break
                    elif d == 'E' and not current_positions & set((surrounding_coords[2], surrounding_coords[4],surrounding_coords[7])):
                        decisions[(erow, ecol + 1)].add((erow, ecol))
                        break
                else:
                    new_positions.add((erow, ecol))
            else:
                new_positions.add((erow, ecol))

        for pos, candidates in decisions.items():
            if len(candidates) == 1 and pos not in new_positions:
                new_positions.add(pos)
            else:
                new_positions.update(candidates)

        self.order = self.order[1:] + self.order[:1]

        return new_positions, (new_positions != current_positions)

def find_bounding_box(positions, dimensions):
    minr, minc = dimensions
    maxr, maxc = 0, 0

    for (r, c) in positions:
        minr = min(minr, r)
        maxr = max(maxr, r)
        minc = min(minc, c)
        maxc = max(maxc, c)

    return (maxr - minr + 1, maxc - minc + 1)

def main(data):
    dimensions, elves = data

    rounds = 0
    moved = True

    diffuse = DiffusionEngine()
    while (rounds < 10) and moved:
        elves, moved = diffuse(elves, dimensions)
        rounds += 1
    height, width = find_bounding_box(elves, dimensions)
    print("Empty ground tiles after 10 rounds:", (height * width) - len(elves))
    while moved:
        elves, moved = diffuse(elves, dimensions)
        rounds += 1
    print("The first round no one moved was:", rounds)

def read_input(stream):
    grove = tuple(map(str.strip, stream.readlines()))
    elves = set((j, i) for (j, row) in enumerate(grove) for (i, c) in enumerate(row) if c == '#')
    return (len(grove), len(grove[0])), elves

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
