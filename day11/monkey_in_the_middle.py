#!/usr/bin/env python3

import sys
import operator
from typing import List, Callable
from functools import reduce
import dataclasses
from pprint import pprint
from copy import deepcopy
from math import gcd

@dataclasses.dataclass
class Monkey:
    items: List[int]
    operation: Callable
    multiplicative: bool
    test_factor: int
    tmonkey: int
    fmonkey: int
    inspections: int

    def whom_to_throw(self, level):
        return self.tmonkey if (level % self.test_factor == 0) else self.fmonkey

    def add_item(self, level):
        self.items.append(level)

    def reset_items(self):
        self.inspections += len(self.items)
        self.items = []

def read_monkey(stream):
    stream.readline()
    items = [int(item) for item in stream.readline().strip().split(':')[-1].split(', ')]
    mult = False
    match stream.readline().split('=')[-1].strip().split():
        case ['old', '+', other]:
            op = operator.add
        case ['old', '*', other]:
            mult = True
            op = operator.mul
        case _:
            raise RuntimeError(f"Unrecognized operation {_}")

    if other == 'old':
        operation = lambda old: op(old, old)
    else:
        k = int(other)
        operation = lambda old,k=k: op(old, k)
    test_factor = int(stream.readline().strip().split(' by ')[1])
    tmonkey = int(stream.readline().strip().split()[-1])
    fmonkey = int(stream.readline().strip().split()[-1])

    return Monkey(items, operation, mult, test_factor, tmonkey, fmonkey, 0)

def read_input(stream):
    monkeys=[]
    while True:
        monkeys.append(read_monkey(stream))
        if stream.readline() == '':
            break
    return monkeys

def advance_round(monkeys, relief_factor=None, mcm=1):
    for monkey in monkeys:
        for i, worry_level in enumerate(monkey.items):
            new_level = monkey.operation(worry_level)
            if relief_factor is None:
                new_level %= mcm
            else:
                new_level //= 3
            who_gets_it = monkey.whom_to_throw(new_level)
            monkeys[who_gets_it].add_item(new_level)
        monkey.reset_items()

def main(data):
    monkeys = data
    mcm = reduce(operator.mul, (m.test_factor for m in monkeys))
    with_relief = deepcopy(monkeys)
    for k in range(20):
        advance_round(with_relief, relief_factor = 3)
    inspections = sorted(m.inspections for m in with_relief)

    print("Monkey business after 20 rounds:", inspections[-2] * inspections[-1])

    without_relief = deepcopy(monkeys)
    for k in range(10000):
        advance_round(without_relief, mcm=mcm)
    inspections = sorted(m.inspections for m in without_relief)
    print(f"Monkey business after 10000 rounds without relief...:", inspections[-2] * inspections[-1])

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
