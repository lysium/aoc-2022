from __future__ import annotations
import sys

from pos import Pos
from util import read_file_lines, signum
from enum import Enum
import os
import re


def main(file):
    part1(file)
    part2(file)


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    RIGHT = 'R'
    LEFT = 'L'


def move(pos: Pos, dir: Direction):
    if dir == Direction.UP:
        dx, dy = 0, -1
    elif dir == Direction.DOWN:
        dx, dy = 0, 1
    elif dir == Direction.LEFT:
        dx, dy = -1, 0
    elif dir == Direction.RIGHT:
        dx, dy = 1, 0
    else:
        raise Exception(f'no such direction {dir}')
    return Pos(pos.x + dx, pos.y + dy)


def is_adjacent(pos1, pos2):
    return abs(pos1.x - pos2.x) <= 1 and abs(pos1.y - pos2.y) <= 1


def move_tail(head, tail):
    """move tail towards head, assuming head and tail are not adjacent."""
    dx = head.x - tail.x
    dy = head.y - tail.y

    if abs(dx) > abs(dy):
        return Pos(head.x + (-signum(dx) * 1), head.y)
    elif abs(dx) < abs(dy):
        return Pos(head.x, head.y + (-signum(dy) * 1))
    else:  # abs(dy) == abs(dx):
        return Pos(head.x + (-signum(dx)), head.y + (-signum(dy)))


def parse_line(line):
    direction, amount = line.split(' ')
    direction = Direction(direction)
    amount = int(amount)
    return amount, direction


def part1(file):
    head = Pos(0, 0)
    tail = Pos(0, 0)
    visited = set()

    for line in read_file_lines(file):
        amount, direction = parse_line(line)
        for i in range(amount):
            head = move(head, direction)
            if not is_adjacent(head, tail):
                tail = move_tail(head, tail)
            visited.add(tail)

    print(len(visited))


def print_rope(rope):
    extra = 2  # extra space around printed grid
    min_pos = Pos(min([knot.x for knot in rope]), min([knot.y for knot in rope]))
    max_pos = Pos(max([knot.x for knot in rope]), max([knot.y for knot in rope]))
    print(f"min: {min_pos}, max: {max_pos}")
    for y in range(min_pos.y-extra, max_pos.y+1+extra):
        for x in range(min_pos.x-extra, max_pos.x+1+extra):
            maybe_knot = [i for i, knot in enumerate(rope) if knot == Pos(x, y)]
            if maybe_knot:
                print(min(maybe_knot), end='')
            else:
                print('.', end='')
        print()


def part2(file):
    rope_length = 10
    rope = [Pos(0, 0) for _ in range(rope_length)]
    visited = set()

    for line in read_file_lines(file):
        amount, direction = parse_line(line)
        for _ in range(amount):
            new_rope = [move(rope[0], direction)]
            for knot in rope[1:]:
                if not is_adjacent(new_rope[-1], knot):
                    knot = move_tail(new_rope[-1], knot)
                new_rope.append(knot)
            rope = new_rope
            visited.add(rope[-1])
    print(len(visited))


if __name__ == "__main__":
    this_script_name = os.path.basename(sys.argv[0])
    m = re.search('(\\d+)\\.py', this_script_name)
    if m:
        day = int(m.group(1))
        input_file = f"input{day:02}.txt"
    else:
        input_file = sys.argv[1]
    main(input_file)
