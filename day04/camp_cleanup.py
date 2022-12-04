#!/usr/bin/env python3

import sys
import string

priorities = {x:((ord(x) - ord('a')) + 1) for x in string.ascii_lowercase} | {x:(ord(x) - ord('A') + 27) for x in string.ascii_uppercase}

def to_set(text_range):
    a, b = text_range.split('-')
    return set(range(int(a), int(b)+1))

def read_input(stream):
    for line in stream:
        first, second = line.strip().split(',')
        yield to_set(first), to_set(second)

def main(data):
    subsets = 0
    overlapping = 0
    for first, second in data:
        if first.issubset(second) or second.issubset(first):
            subsets += 1
            overlapping += 1
        elif first & second:
            overlapping += 1
    print("Total fully overlapping pairs:", subsets)
    print("Total partial or fully overlapping pairs:", overlapping)

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
