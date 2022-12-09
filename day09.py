from __future__ import annotations
import sys
from util import read_file_lines
from dataclasses import dataclass
from enum import Enum
from anytree import NodeMixin
from functools import total_ordering


def main(file):
    part1(file)
    part2(file)


@dataclass
@total_ordering
class Pos:
    x: int
    y: int

    def __hash__(self):
        return 113 * self.x + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y


class Direction(Enum):
    UP='U'
    DOWN='D'
    RIGHT='R'
    LEFT='L'


def move(pos: Pos, dir: Direction):
    if dir == Direction.UP:
        dx, dy = 0,-1
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
    """move tail towards head, assuming head and tail are just not adjacent."""
    dx = head.x - tail.x
    dy = head.y - tail.y

    if dx == 2:  # tail goes LEFT of head
        return Pos(head.x - 1, head.y + 0)
    elif dx == -2:  # tail goes RIGHT of head
        return Pos(head.x + 1, head.y + 0)
    elif dy == 2:  # tail goes UP of head
        return Pos(head.x + 0, head.y - 1)
    elif dy == -2: # tail goes DOWN of head
        return Pos(head.x + 0, head.y + 1)
    else:
        raise Exception(f'unexcepted dx/dy: {dx}, {dy}')


def part1(file):
    head = Pos(0, 0)
    tail = Pos(0, 0)
    visited = set()

    for line in read_file_lines(file):
        direction, amount = line.split(' ')
        direction = Direction(direction)
        amount = int(amount)
        for i in range(amount):
            head = move(head, direction)
            if not is_adjacent(head, tail):
                tail = move_tail(head, tail)
            visited.add(tail)

    print(len(visited))


def part2(file):
    for line in read_file_lines(file):
        pass


if __name__ == "__main__":
    day = 9
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
