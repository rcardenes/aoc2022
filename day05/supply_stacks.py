#!/usr/bin/env python3

import sys
import string
import copy

def read_input(stream):
    stack_lines = []

    for line in stream:
        if not line.strip():
            break
        stack_lines.append(line)

    nstacks = len(stack_lines[-1].split())
    stacks = [list() for k in range(nstacks)]
    for stack_line in reversed(stack_lines[:-1]):
        for n in range(nstacks):
            try:
                l = stack_line[(n*4) + 1]
                if l.strip():
                    stacks[n].append(l)
            except IndexError:
                ...

    moves = []
    for line in stream:
        bits = line.split()
        moves.append((int(bits[1]), int(bits[3])-1, int(bits[5])-1))

    return stacks, moves

def move_crates(stacks, n, a, b):
    for k in range(n):
        stacks[b].append(stacks[a].pop())

def move_crates_9001(stacks, n, a, b):
    stacks[b].extend(stacks[a][-n:])
    stacks[a] = stacks[a][:-n]

def main(data):
    orig_stacks, instructions = data

    stacks_9000 = copy.deepcopy(orig_stacks)
    stacks_9001 = copy.deepcopy(orig_stacks)
    for inst in instructions:
        move_crates(stacks_9000, *inst)
        move_crates_9001(stacks_9001, *inst)

    print("Top crates for CrateMover 9000:", ''.join(st[-1] for st in stacks_9000))
    print("Top crates for CrateMover 9001:", ''.join(st[-1] for st in stacks_9001 if st))


if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
