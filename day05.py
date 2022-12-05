import sys
from util import read_file_lines
from enum import Enum
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


class State(Enum):
    READ_CRATES = 1,
    READ_INSTRUCTIONS = 2


def execute_input(file, crate_mover):
    state = State.READ_CRATES
    crates = []
    crate_lines = []
    for line in read_file_lines(file):
        if state == State.READ_CRATES:
            if line == "":
                stack_labels = re.split('\s+', crate_lines[-1])[1:-1]
                no_stacks = len(stack_labels)
                max_stack_height = len(crate_lines) - 1
                for x in range(no_stacks):
                    stack = []
                    for y in range(max_stack_height):
                        cargo = crate_lines[y][1+4*x]
                        if cargo != ' ':
                            stack.append(cargo)
                    stack.reverse()
                    crates.append(stack)
                state = State.READ_INSTRUCTIONS
            else:
                crate_lines.append(line)
        elif state == State.READ_INSTRUCTIONS:
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
