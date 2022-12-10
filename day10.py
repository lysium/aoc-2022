from __future__ import annotations
import sys
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin
from enum import Enum
import os
import re


def main(file):
    part1(file)
    part2(file)


class Cmd(Enum):
    ADDX = "addx"
    NOOP = "noop"


@dataclass
class Instruction:
    cmd: Cmd
    arg: any   # Optional


def instruction_from_line(line):
    words = line.split(' ')
    cmd = Cmd(words[0])
    if cmd == Cmd.ADDX:
        arg = int(words[1])
    else:
        arg = None
    return Instruction(cmd, arg)


def instructions_from_file(file):
    return [instruction_from_line(line) for line in read_file_lines(file)]


def compute(register, instructions):
    log = []   # value of register at the beginning of the Xth cycle

    def tick():
        log.append(register)

    while instructions:
        instruction = instructions.pop(0)
        if instruction.cmd == Cmd.NOOP:
            tick()
        elif instruction.cmd == Cmd.ADDX:
            tick()
            tick()
            register += instruction.arg
    tick()  # cheat to register final register value...
    return log


def part1(file):
    register = 1
    instructions = instructions_from_file(file)
    log = compute(register, instructions)
    signal_strength = 0
    for i in range(19, 220, 40):
        print(f"{i+1} \t {log[i]} \t {log[i] * (i+1)}")
        signal_strength += log[i] * (i+1)
    print(signal_strength)


def part2(file):
    for line in read_file_lines(file):
        pass


if __name__ == "__main__":
    this_script_name = os.path.basename(sys.argv[0])
    m = re.search('(\\d+)\\.py', this_script_name)
    if len(sys.argv) <= 1 and m:
        day = int(m.group(1))
        input_file = f"input{day:02}.txt"
    else:
        input_file = sys.argv[1]

    main(input_file)
