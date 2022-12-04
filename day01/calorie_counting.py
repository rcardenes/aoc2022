import sys

def read_input(stream):
    total = 0
    for line in stream:
        if not line.strip():
            yield total
            total = 0
        else:
            total += int(line)
    else:
        yield total

def main(data):
    list_of_calories = list(data)
    list_of_calories.sort()
    print("Max calories from any elf:", list_of_calories[-1])
    print("Total calories from the top 3 carriers:", sum(list_of_calories[-3:]))

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))
