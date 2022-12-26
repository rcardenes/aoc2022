#!/usr/bin/env python3
import sys
from itertools import zip_longest
from pprint import pprint

dmapping = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
fmapping = {0: 0, 1: 1, 2: 2, 3: -2, 4: -1}
rmapping = {0: '0', 1: '1', 2: '2', 3: '=1', 4: '-1', 5: '01', 6: '11'}

def snafu_to_decimal(text):
    return sum(tuple((dmapping[c] * (5**i)) for (i, c) in enumerate(reversed(text))))

def decimal_to_snafu(number):
    if number == 0:
        return '0'

    digits = []
    i = 0
    carry = 0
    while number > 5:
        d = (number % 5) + carry
        carry = 1 if d > 2 else 0
        digits.append(rmapping[d % 5][0])
        number //= 5
        i += 1
    if number > 0:
        digits.append(rmapping[number + carry])
    return ''.join(reversed(''.join(digits)))

def main(data):
    total = sum(snafu_to_decimal(req) for req in data)
    print("The total fuel requirements is:", decimal_to_snafu(total))

def read_input(stream):
    requirements = tuple(line.strip() for line in stream.readlines())
    return requirements

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
