#!/usr/bin/env python3

import sys

def read_input(stream):
    for line in stream:
        yield line.strip().split()

class Simulator:
    def __init__(self):
        self.trace = [1]
        self.cycles = 0
        self.X = 1

    def addx(self, x):
        self.trace.extend([self.X] * 3)
        self.X += x
        self.trace.append(self.X)
        self.cycles += 2

    def noop(self):
        self.trace.extend([self.X, self.X])
        self.cycles += 1

    def sum_sig_strength(self):
        return sum (self.trace[(k * 2) - 1] * k for k in range(20, 221, 40))

    def print_screen(self):
        def illuminated(cycle, hor_pixel):
            x = self.trace[(cycle * 2) - 1]
            return (x - 1) <= hor_pixel <= (x+1)
        pixels = ''.join([('#' if illuminated(k+1, k % 40) else '.') for k in range(240)])
        for k in range(0, 201, 40):
            print(pixels[k:k+40])

def main(data):
    sim = Simulator()
    for bits in data:
        match bits:
            case ['noop']:
                sim.noop()
            case ['addx', x]:
                sim.addx(int(x))
    print("Signal strength:", sim.sum_sig_strength())
    sim.print_screen()


if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
