#!/usr/bin/env python3

import sys
import string
import copy

def read_input(stream):
    return stream.read()

def find_marker(data, length):
    pos = length
    while True:
        if len(set(data[pos-length:pos])) == length:
            return pos
        pos += 1

def main(data):
    print("Pos of last element from the marker:", find_marker(data, 4))
    print("Pos of last element from the marker:", find_marker(data, 14))

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
