import sys
from util import read_file_lines
import re


def main(file):
    part1(file)
    part2(file)


def crate_mover_9001(crates, amount, start, end):
    return crate_mover_helper(crates, amount, start, end, byOne=False)


def crate_mover_9000(crates, amount, start, end):
    return crate_mover_helper(crates, amount, start, end, byOne=True)


def crate_mover_helper(crates, amount, start, end, byOne):
    moved_crates = crates[start][-amount:]
    crates[start] = crates[start][:-amount]
    if byOne:
        moved_crates.reverse()
    crates[end].extend(moved_crates)
    return crates


def execute_input(file, crate_mover):
    crates = [
        ["C", "Z", "N", "B", "M", "W", "Q", "V"],
        ["H", "Z", "R", "W", "C", "B"],
        ["F", "Q", "R", "J"],
        ["Z", "S", "W", "H", "F", "N", "M", "T"],
        ["G", "F", "W", "L", "N", "Q", "P"],
        ["L", "P", "W"],
        ["V", "B", "D", "R", "G", "C", "Q", "J"],
        ["Z", "Q", "N", "B", "W"],
        ["H", "L", "F", "C", "G", "T", "J"],
    ]
    # skip reading creates for now
    read_instructions = False
    for line in read_file_lines(file):
        if line == "":
            read_instructions = True
        elif read_instructions:
            m = re.match("move (\d+) from (\d+) to (\d+)", line)
            if not m:
                print(f"no match: {line}")
                raise Exception()
            amount = int(m.group(1))
            stack_start = int(m.group(2)) - 1
            stack_end = int(m.group(3)) - 1
            crate_mover(crates, amount, stack_start, stack_end)

    result = ""
    for crate in crates:
        if len(crate) > 0:
            result += crate[-1]
    print(result)


def part1(file):
    execute_input(file, crate_mover_9000)


def part2(file):
    execute_input(file, crate_mover_9001)


if __name__ == "__main__":
    day = 5
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
