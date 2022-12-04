import sys

shape_value = {
        'A': 1,
        'B': 2,
        'C': 3
        }

wins_over = {
        'A': 'C',
        'B': 'A',
        'C': 'B'
        }

trounced_by = {
        'A': 'B',
        'B': 'C',
        'C': 'A'
        }

code = {
        'X': 'A',
        'Y': 'B',
        'Z': 'C'
        }

def read_input(stream):
    for line in stream:
        a, b = line.strip().split()
        yield a, b

def calc_outcome(a, b):
    base_points = shape_value[b]
    if a == b:
        return base_points + 3
    elif wins_over[a] == b:
        return base_points
    else:
        return base_points + 6

def calc_real_outcome(a, b):
    if b == 'X':
        return calc_outcome(a, wins_over[a])
    elif b == 'Y':
        return calc_outcome(a, a)
    else:
        return calc_outcome(a, trounced_by[a])

def main(data):
    pairs = list(read_input(stream))
    total_points_orig = sum(calc_outcome(a, code[b]) for (a, b) in pairs)
    total_points_modified = sum(calc_real_outcome(*pair) for pair in pairs)
    print("Total points following original guide:", total_points_orig)
    print("Total points following actual guide:", total_points_modified)

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
