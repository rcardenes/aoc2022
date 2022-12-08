#!/usr/bin/env python3

import operator
import sys
import numpy as np
from functools import reduce

def read_input(stream):
    lines = []
    for line in stream:
        lines.append(list(int(c) for c in line.strip()))
    return np.array(lines, dtype=int)

def markVisibleFromTop(data, visibilityMap):
    maximums = np.maximum.accumulate(data)
    for n, (dRow, mRow) in enumerate(zip(data[1:], maximums[:-1])):
        visibilityMap[n] = np.logical_or(visibilityMap[n], mRow < dRow)

def updateVisibilityMap(data, visibilityMap):
    markVisibleFromTop(data[:-1, 1:-1], visibilityMap)
    markVisibleFromTop(data.T[:-1, 1:-1], visibilityMap.T)
    markVisibleFromTop(np.flipud(data)[:-1, 1:-1], np.flipud(visibilityMap))
    markVisibleFromTop(np.fliplr(data).T[:-1, 1:-1], np.fliplr(visibilityMap).T)

def countVisibleFromAllEdges(data):
    shp = data.shape
    edges = (shp[0]*2 + shp[1]*2) - 4
    visibilityMap = np.zeros((shp[0] - 2, shp[1] - 2), dtype=bool)
    updateVisibilityMap(data, visibilityMap)
    return edges + visibilityMap.sum()

def scenicScore(data, row, column):
    element = data[row,column]
    shp = data.shape

    def count(coords, lim, diff):
        vt = 0
        while not np.array_equal(coords, lim):
            coords += diff
            vt += 1
            if data[coords[0], coords[1]] >= element:
                break
        return vt

    vis_trees = [
            count(np.array([row, column]), np.array([0, column]), np.array([-1, 0])),
            count(np.array([row, column]), np.array([shp[0] - 1, column]), np.array([1, 0])),
            count(np.array([row, column]), np.array([row, 0]), np.array([0, -1])),
            count(np.array([row, column]), np.array([row, shp[1] - 1]), np.array([0, 1]))
            ]

    return reduce(operator.mul, vis_trees)

def maxScenicScore(data):
    xv, yv = np.meshgrid(range(data.shape[0]), range(data.shape[1]))
    return max([scenicScore(data, r, c) for (c, r) in zip(xv[1:-1,1:-1].flatten(), yv[1:-1,1:-1].flatten())])

def main(data):
    print("Visible from edges:", countVisibleFromAllEdges(data))
    print("Max scenic score:", maxScenicScore(data))

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
