import sys
from util import read_file_lines


def main(file):
    part1(file)
    part2(file)


def part1(file):
    for line in read_file_lines(file):
        pass


def part2(file):
    for line in read_file_lines(file):
        pass


if __name__ == "__main__":
    day = 4
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
