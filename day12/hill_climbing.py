#!/usr/bin/env python3

import sys
from operator import itemgetter
from pprint import pprint

INFINITY = 1000000

def char_to_elevation(c):
    return ord(c) - ord('a')

class Node:
    def __init__(self, level):
        self.level = level
        if level == 'S':
            self.elevation = 0
        elif level == 'E':
            self.elevation = char_to_elevation('z')
        else:
            self.elevation = char_to_elevation(level)
        self.coords = None
        self.is_target = level == 'E'
        self._neighbors = set()
        self.visited = False

    def set_coords(self, row, col):
        self.coords = (row, col)

    def maybe_add_vertex(self, node):
        distance = self.distance_to(node)
        if distance > -2:
            self._neighbors.add((self.distance_to(node), node))

    def repr_elevation(self):
        return chr(ord('a') + self.elevation)

    def distance_to(self, node):
        # Don't connect anything to the starting point, to avoid
        # loops
        if node.level == 'S':
            return INFINITY
        return self.elevation - node.elevation

    def neighbors(self):
        return [x[1] for x in self._neighbors]

    def __repr__(self):
        return self.level + f"({''.join(v[1].level for v in self._neighbors)})"

def read_input(stream):
    raw_input = [[Node(l) for l in line.strip()]
                 for line in stream.readlines()]

    return raw_input

def solve(starting, dist, prev, raw_input=None):
    """
    Adapted Dijkstra algorithm. More like a BFS, with the optimizations in place.
    """
    Q = {starting}
    dist[starting] = 0

    if raw_input:
        print_trace(raw_input, dist, prev)
    while Q:
        u, dth = sorted(((k, dst) for (k, dst) in dist.items() if k in Q), key=itemgetter(1))[0]
        Q.remove(u)
        if u.is_target:
            return dist[u]

        alt = dist[u] + 1 # Don't care about the edge distance, really
        for v in u.neighbors():
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                Q.add(v)
                if raw_input:
                    print_trace(raw_input, dist, prev)

    return INFINITY

def init(raw_input):
    rows = len(raw_input)
    cols = len(raw_input[0])

    max_row = rows - 1
    max_col = cols - 1

    graph = None
    target = None
    low_points = set()
    dist = {}
    prev = {}

    for r in range(rows):
        for c in range(cols):
            n = raw_input[r][c]
            n.set_coords(r, c)
            if n.level == 'S':
                graph = n
            else:
                if n.level == 'a':
                    low_points.add(n)
                elif n.level == 'E':
                    target = n
            dist[n] = INFINITY
            prev[n] = None

            if r > 0:
                n.maybe_add_vertex(raw_input[r-1][c])
            if r < max_row:
                n.maybe_add_vertex(raw_input[r+1][c])

            if c > 0:
                n.maybe_add_vertex(raw_input[r][c-1])
            if c < max_col:
                n.maybe_add_vertex(raw_input[r][c+1])

    return graph, target, low_points, dist, prev

def prev_symbol(current, prev):
    if prev is None:
        return '.'
    else:
        ccoords, pcoords = current.coords, prev.coords
        if pcoords[0] < ccoords[0]:
            return '^'
        elif pcoords[0] > ccoords[0]:
            return 'v'
        elif pcoords[1] < ccoords[1]:
            return '<'
        else:
            return '>'

def print_route(array, starting, target, prev, empty=True):
    route = {target}
    u = target
    while u != starting:
        u = prev[u]
        route.add(u)

    for row in array:
        rep = []
        for k in row:
            if k is target:
                rep.append('E')
            elif k is starting:
                rep.append('S')
            elif k in route:
                rep.append(prev_symbol(k, prev[k]))
            else:
                rep.append('.' if empty else k.repr_elevation())
        print(''.join(rep))

def main(data):
    graph, target, low_points, dist, prev = init(data)
    solve(graph, dist, prev)
    min_distance = dist[target]
    print("Steps to the place with best signal:", min_distance)
    print_route(data, graph, target, prev)
    new_shortest = None
    for k in low_points:
        new_attempt = solve(k, dist, prev)
        if new_attempt < min_distance:
            min_distance = new_attempt
            new_shortest = k
    if not new_shortest:
        print("No changes in route")
    else:
        print("Absolute minimum distance:", min_distance)
        print_route(data, new_shortest, target, prev)

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
