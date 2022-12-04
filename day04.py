import sys
from util import read_file_lines


def main(file):
    part1(file)
    part2(file)


class Assignment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, other):
        """true if this assignment fully contains the other"""
        return self.start <= other.start and self.end >= other.end


def assignment_from_string(pair):
    (start, end) = pair.split('-')
    return Assignment(int(start), int(end))


def part1(file):
    count = 0
    for line in read_file_lines(file):
        (pair1, pair2) = line.split(',')
        assignment1 = assignment_from_string(pair1)
        assignment2 = assignment_from_string(pair2)
        if assignment1.contains(assignment2) or assignment2.contains(assignment1):
            count +=1
    print(count)


def part2(file):
    for line in read_file_lines(file):
        pass


if __name__ == "__main__":
    day = 4
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
