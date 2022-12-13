#!/usr/bin/env python3
import sys
from pprint import pprint
from functools import cmp_to_key

def read_input(stream):
    pairs = []
    while True:
        pairs.append((eval(stream.readline().strip()),
                      eval(stream.readline().strip())))
        if not stream.readline():
            break
    return pairs

def right_order(left, right):
    for a, b in zip(left, right):
        if isinstance(a, int) and isinstance(b, int):
            if a < b:
                return -1
            elif a > b:
                return 1
        else:
            if isinstance(a, int):
                a = [a]
            elif isinstance(b, int):
                b = [b]
            res = right_order(a, b)
            if res != 0:
                return res

    if len(left) != len(right):
        return -1 if len(left) < len(right) else 1

    return 0

def main(data):
    ro = [i for (i, pair) in enumerate(data, 1) if right_order(*pair) < 0]
    print("Sum of the indices of packet pairs in right order:", sum(ro))
    allpackets = sum(data, ()) + ([[2]], [[6]])
    indices = []
    for i, l in enumerate(sorted(allpackets, key=cmp_to_key(right_order)), 1):
        if l == [[2]] or l == [[6]]:
            indices.append(i)
    print("Decoder key:", indices[0] * indices[1])

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
