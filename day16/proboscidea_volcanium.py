#!/usr/bin/env python3
import sys
import re
import itertools
from collections import defaultdict
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any
from pprint import pprint
from time import time
import operator
from functools import reduce

@dataclass
class Node:
    name: str
    rate: int
    leads_to: list["Node"]
    distances: dict

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Node(name='{self.name}', rate={self.rate}, leads_to=({', '.join(n.name for n in self.leads_to)}))"

def simulate_travel(root, waypoints, rest=()):
    total_released = 0
    steps_left = 30
    current = root
    for target in waypoints:
        dist = current.distances[target]
        steps_left -= dist + 1
        if steps_left < 1:
            break
        total_released += target.rate * steps_left
        current = target

    for instant in rest:
        dist = current.distances[instant]
        if steps_left > dist:
            total_released += instant.rate * (steps_left - dist + 1)

    return total_released

@dataclass(order=True)
class PrioritizeItem:
    priority: int
    payload: Any=field(compare=False)

def find_optimal_route(root):
    target_list = set(root.distances)
    best_solution = None
    # This gives us a lower bound. We won't find anything worse than
    # this, so...
    B = 0

    # Generate a first set of potential partial solutions
    q = PriorityQueue()
    for t in target_list:
        release = simulate_travel(root, [t], target_list - {t})
        q.put(PrioritizeItem(-release, [t]))

    generated = len(target_list)
    rejected = 0

    while not q.empty():
        candidate = q.get()
        NB = -candidate.priority
        if B > NB:
            rejected += 1
            continue
        # New generation of possible solutions
        p = candidate.payload
        left = target_list - set(p)
        if len(left) < 5:
            for final in itertools.permutations(left, r=len(left)):
                generated += 1
                newp = p + list(final)
                release = simulate_travel(root, newp)
                if release > B:
                    B = release
                    best_solution = newp
                else:
                    rejected += 1
        else:
            for t in left:
                generated += 1
                newp = p + [t]
                release = simulate_travel(root, newp, left - {t})
                if release > B:
                    q.put(PrioritizeItem(-release, newp))
                else:
                    rejected += 1
    return B, best_solution

def solve_and_print(data):
    now = time()
    released, best_solution = find_optimal_route(data)
    then = time()
    print(f"Pressure released: {released}")
    print(f"Computed in {then - now} seconds")

def main(data):
    solve_and_print(data)

def dijkstra(root, all_nodes):
    INF = 10000000000
    Q = PriorityQueue()
    dist = {}
    prev = {}
    for n in all_nodes:
        dist[n] = INF
        prev[n] = None
    dist[root] = 0
    Q.put(PrioritizeItem(0, root))
    while not Q.empty():
        candidate = Q.get()
        dist_to_current, current = candidate.priority, candidate.payload
        # No weights for edges, so just add 1
        alt = dist_to_current + 1
        for adjacent in current.leads_to:
            if dist[adjacent] > alt:
                dist[adjacent] = alt
                prev[adjacent] = current
                Q.put(PrioritizeItem(alt, adjacent))

    return dist, prev

def read_input(stream):
    pattern = re.compile('Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)')
    nodes = {}
    leads_to = {}

    # This gets us a basic form of the graph.
    working = []
    for line in stream:
        name, rate, others = pattern.match(line).groups()
        node = Node(name, int(rate), [], {})
        nodes[name] = node
        leads_to[node] = others.split(', ')
        if node.rate > 0:
            working.append(node)
    for node, others in leads_to.items():
        node.leads_to = [nodes[n] for n in others]

    # We're not really interested in the valves that give no flow, so we should
    # somehow simplify the graph. This will also reduce the number of steps later
    root = nodes['AA']
    for name, node in nodes.items():
        dist, prev = dijkstra(node, nodes.values())
        node.distances = {n:d for (n, d) in dist.items() if n in working}

    return root

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
