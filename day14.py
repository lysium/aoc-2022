from __future__ import annotations
import sys

from pos import Pos
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin
import os
import re
from vec import Vec, UP, DOWN, LEFT, RIGHT


def main(file):
    part1(file)
    part2(file)


def part1(file):
    lines_of_rock = []
    for line in read_file_lines(file):
        points = [Pos(int(x), int(y)) for x,y in [xy.split(',') for xy in line.split(' -> ')]]
        lines_of_rock.append(points)
    print(lines_of_rock)
    abyss_y = max([max([pos.y for pos in line]) for line in lines_of_rock])
    # print(abyss_y)

    rock = set()
    for line in lines_of_rock:
        for start_pos, end_pos in zip(line, line[1:]):
            if start_pos.x == end_pos.x: # horizontal line
                vec = DOWN if start_pos.y < end_pos.y else UP
            elif start_pos.y == end_pos.y:  # vertical line
                vec = RIGHT if start_pos.x < end_pos.x else LEFT
            else:
                raise Exception("not a straight line")
            rock.add(start_pos)
            pos = start_pos
            while pos != end_pos:
                pos += vec
                rock.add(pos)

    count = 0
    SW = Vec(-1, 1)
    SE = Vec(1, 1)
    abyss_reached = False
    while not abyss_reached:
        sand = Pos(500,0)
        while True:
            new_pos = sand + DOWN
            if new_pos.y > abyss_y:
                abyss_reached = True
                break
            if new_pos in rock:
                new_pos = sand + SW
                if new_pos in rock:
                    new_pos = sand + SE
                    if new_pos in rock:
                        rock.add(sand)
                        count = count + 1
                        break
            sand = new_pos
    print(count)


def part2(file):
    for line in read_file_lines(file):
        pass


def input_file_from_argv(argv):
    this_script_name = os.path.basename(argv[0])
    m = re.search('(\\d+)\\.py', this_script_name)
    if len(argv) <= 1 and m:
        day = int(m.group(1))
        return f"input{day:02}.txt"
    else:
        return argv[1]



if __name__ == "__main__":
    input_file = input_file_from_argv(sys.argv)
    main(input_file)
