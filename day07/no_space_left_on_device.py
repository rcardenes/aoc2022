#!/usr/bin/env python3

import sys
from collections import namedtuple
from pprint import pprint

Directory = namedtuple('Directory', 'contents size')

def updateSizes(member):
    if isinstance(member, File):
        return member
    else:
        new_contents = {k:updateSizes(v) for (k,v) in member.contents.items()}
        return Directory(member.parent,
                         member.name,
                         new_contents,
                         sum(v.size for v in new_contents.values()))

def read_input(stream):
    dirs = {}
    current = ''

    def switch_to(dir_name):
        match dir_name:
            case '/':
                path = '/'
            case '..':
                path = (current.rpartition('/')[0]) or '/'
            case _:
                path = ('/' + name) if current == '/' else  '/'.join((current, dir_name))
        if path not in dirs:
            dirs[path] = Directory(set(), 0)
        return path

    def updateSizes(node_dir, node, size):
        the_dir = dirs[node_dir]
        if node not in the_dir:
            dirs[node_dir] = Directory(the_dir.contents | {node},
                                       the_dir.size + size)
            while node_dir != '/':
                node_dir = node_dir.rpartition('/')[0] or '/'
                the_dir = dirs[node_dir]
                dirs[node_dir] = Directory(the_dir.contents,
                                           the_dir.size + size)

    current = switch_to('/')
    for line in stream:
        bits = line.strip().split()
        match bits:
            case ['$', 'cd', '/']:
                current = switch_to('/')
            case ['$', 'cd', '..']:
                current = switch_to('..')
            case ['$', 'cd', name]:
                current = switch_to(name)
            case ['$', 'ls']:
                # Do nothing, we're listing
                ...
            case ['dir', name]:
                # Ignore this one as well, not relevant in our structure representation
                ...
            case [size, name]:
                # We're listing a regular file
                updateSizes(current, name, int(size))

    return dirs

def sumSizesUpTo(threshold, root):
    return sum(v.size for v in root.values() if v.size <= threshold)

def findSizesEqualOrOver(threshold, root):
    return [v.size for v in root.values() if v.size >= threshold]

FILESYSTEM_SIZE = 70000000
NEEDED_UNUSED = 30000000

def main(data):
    print("Total in dirs up to 100000:", sumSizesUpTo(100000, data))
    currentFree = FILESYSTEM_SIZE - data['/'].size
    print("Smallest directory size that gives us the wanted space:",
          sorted(findSizesEqualOrOver(NEEDED_UNUSED - currentFree, data))[0])

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
