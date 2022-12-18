#!/usr/bin/env python3
import sys
from collections import defaultdict
from time import time
from pprint import pprint
from itertools import product

def generate_surrounding(x, y, z):
    return {
            (x-1, y, z),
            (x+1, y, z),
            (x, y-1, z),
            (x, y+1, z),
            (x, y, z-1),
            (x, y, z+1)
            }

def find_free_surfaces(cubes):
    fs_reg = {}
    for cube in cubes:
        x, y, z = cube
        variations = generate_surrounding(x, y, z)
        free_faces = variations
        for var in variations.copy():
            if var in fs_reg:
                fs_reg[var].remove(cube)
                free_faces.remove(var)
        fs_reg[cube] = free_faces
    return sum(len(v) for v in fs_reg.values()), fs_reg

def find_isolated(struct):
    mincoord = 10000000
    maxcoord = 0
    for k in struct:
        mincoord = min(mincoord, *k)
        maxcoord = max(maxcoord, *k)

    mincoord -= 1
    maxcoord += 1
    reachable = defaultdict(set)
    generated = set()
    seeds = set(product((mincoord, maxcoord), repeat=3))
    generated.update(seeds)
    while seeds:
        seed = seeds.pop()
        surrounding = set((x, y, z) for (x, y, z) in generate_surrounding(*seed)
                          if (x, y, z) not in generated and
                             (mincoord <= x <= maxcoord) and
                             (mincoord <= y <= maxcoord) and
                             (mincoord <= z <= maxcoord))
        for sr in surrounding:
            if sr in struct:
                reachable[sr].add(seed)
            else:
                generated.add(sr)
                seeds.add(sr)
    return sum(len(v) for v in reachable.values())


def main(data):
    free_surfaces, structure = find_free_surfaces(data)
    print("Total surface area:", free_surfaces)
    esa = find_isolated(structure)
    print("Exterior surface area:", esa)

def read_input(stream):
    cube_coords = [tuple(int(k) for k in line.split(',')) for line in stream]
    return cube_coords

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
