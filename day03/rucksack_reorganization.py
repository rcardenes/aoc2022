#!/usr/bin/env python3

import sys
import string

priorities = {x:((ord(x) - ord('a')) + 1) for x in string.ascii_lowercase} | {x:(ord(x) - ord('A') + 27) for x in string.ascii_uppercase}

def read_input(stream):
    for line in stream:
        sline = line.strip()
        lline = len(sline) // 2
        yield sline[:lline], sline[lline:]

def get_common(h1, h2):
    return set(h1) & set(h2)

def main(data):
##    pairs = list(read_input(stream))
#    total_points_orig = sum(calc_outcome(a, code[b]) for (a, b) in pairs)
#    total_points_modified = sum(calc_real_outcome(*pair) for pair in pairs)
#    print("Total points following original guide:", total_points_orig)
#    print("Total points following actual guide:", total_points_modified)
    total_prio_common = 0
    total_prio_badges = 0
    group = []
    for fhalf, shalf in data:
        total_prio_common += priorities[get_common(fhalf, shalf).pop()]
        group.append(fhalf + shalf)
        if len(group) == 3:
            total_prio_badges += priorities[get_common(group[0], get_common(group[1], group[2])).pop()]
            group = []

    print(f"Total priorities from common elements: {total_prio_common}")
    print(f"Total priorities from badges: {total_prio_badges}")

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
