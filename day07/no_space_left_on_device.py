#!/usr/bin/env python3

import sys
from collections import namedtuple

Directory = namedtuple('Directory', 'parent name contents size')
File = namedtuple('File', 'name size')

def sizeOf(member):
    if isinstance(member, File):
        return member.size
    else:
        return sum(sizeOf(m) for m in member.contents.values())

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
    root = Directory(None, '/', {}, None)
    current = root
    listing = False
    for line in stream:
        bits = line.strip().split()
        match bits:
            case ['$', 'cd', '/']:
                current = root
            case ['$', 'cd', '..']:
                current = current.parent
            case ['$', 'cd', name]:
                current = current.contents[name]
            case ['$', 'ls']:
                # Do nothing, we're listing
                ...
            case ['dir', name]:
                # Listing a directory
                if name not in current.contents:
                    current.contents[name] = Directory(current, name, {}, 0)
            case [size, name]:
                # We're listing a regular file
                current.contents[name] = File(name, int(size))

    return updateSizes(root)

def sumSizesUpTo(threshold, root):
    subdirs = [v for v in root.contents.values() if isinstance(v, Directory)]
    sumHere = sum(v.size for v in subdirs if v.size <= threshold)
    sumRecur = sum(sumSizesUpTo(threshold, v) for v in subdirs)
    return sumHere + sumRecur

def findSizesEqualOrOver(threshold, root):
    if root.size < threshold:
        return []
    result = [root.size]
    for v in root.contents.values():
        if isinstance(v, Directory):
            result += findSizesEqualOrOver(threshold, v)

    return result

FILESYSTEM_SIZE = 70000000
NEEDED_UNUSED = 30000000

def main(data):
    print("Total in dirs up to 100000:", sumSizesUpTo(100000, data))
    currentFree = FILESYSTEM_SIZE - data.size
    print("Smallest directory size that gives us the wanted space:",
          sorted(findSizesEqualOrOver(NEEDED_UNUSED - currentFree, data))[0])

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
