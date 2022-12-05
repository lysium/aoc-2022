import sys
from enum import Enum
import re
from dataclasses import dataclass


def main(file):
    execute_input(file, crate_mover_9000)
    execute_input(file, crate_mover_9001)


def crate_mover_9001(crates, instruction):
    return crate_mover_helper(crates, instruction, byOne=False)


def crate_mover_9000(crates, instruction):
    return crate_mover_helper(crates, instruction, byOne=True)


def crate_mover_helper(crates, instruction, byOne):
    amount = instruction.amount
    start = instruction.stack_start
    end = instruction.stack_end
    moved_crates = crates[start][-amount:]
    crates[start] = crates[start][:-amount]
    if byOne:
        moved_crates.reverse()
    crates[end].extend(moved_crates)
    return crates


def execute_input(file, crate_mover):
    f = open(file, 'r')
    crates = read_crates(f)
    for instruction in read_instructions(f):
        crates = crate_mover(crates, instruction)
    result = top_cargo(crates)
    print(result)


def read_crates(file):
    crate_lines = read_crate_lines(file)
    return crates_from_crate_lines(crate_lines)


def crates_from_crate_lines(crate_lines):
    crates = []
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
    return crates


@dataclass
class Instruction:
    amount: int
    stack_start: int
    stack_end: int


def read_instructions(f):
    while True:
        line = f.readline()
        if line == '':
            break

        m = re.match("move (\d+) from (\d+) to (\d+)", line)
        if not m:
            print(f"no match: {line}")
            raise Exception()
        amount = int(m.group(1))
        stack_start = int(m.group(2)) - 1
        stack_end = int(m.group(3)) - 1
        yield Instruction(amount, stack_start, stack_end)


def top_cargo(crates):
    result = ""
    for crate in crates:
        if len(crate) > 0:
            result += crate[-1]
    return result


def read_crate_lines(file):
    crate_lines = []
    while True:
        line = file.readline().strip('\n')
        if line == "":
            break
        crate_lines.append(line)
    return crate_lines


if __name__ == "__main__":
    day = 5
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
