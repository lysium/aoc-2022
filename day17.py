from __future__ import annotations
import sys

from pos import Pos
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin
import os
import re

from vec import Vec

debug = False

def main(file):
    part1(file)
    part2(file)


@dataclass(frozen=True)
class Shape:
    rocks: [Vec]

def make_shape(rocks):
    return Shape([Vec(dx, dy) for dx, dy in zip(*[iter(rocks)] * 2)])

SHAPES = [
    make_shape([0,0, 1,0, 2,0, 3,0]),   # ####
    make_shape([      1,2,              # .#.
                0,1,  1,1, 2,1,         # ###
                      1,0         ]),   # .#.
    make_shape([          2,2,      # ..#
                          2,1,      # ..#
                0,0, 1,0, 2,0]),    # ###
    make_shape([0,3,    # #
                0,2,    # #
                0,1,    # #
                0,0]),  # #
    make_shape([0,1, 1,1,   # ##
                0,0, 1,0])  # ##
]


LEFT = Vec(-1, 0)
RIGHT = Vec(1, 0)
DOWN = Vec(0, -1)


def is_occupied(pos, shape, occupied):
    for rock in shape.rocks:
        rock_pos = pos + rock
        if rock_pos in occupied:
            return True
    return False

TOWER_WIDTH = 7

def is_in_bounds(pos, shape):
    for rock in shape.rocks:
        rock_pos = pos + rock
        if not (0 < rock_pos.x < TOWER_WIDTH + 1) or rock_pos.y <= 0:
            return False
    return True


def print_tower(shape, shape_pos, occupied_rocks):
    max_height = max([p.y for p in occupied_rocks.keys()] + [shape_pos.y])
    max_height += max([r.dy for r in shape.rocks])
    for y in range(max_height, 0, -1):
        print('|', end='')
        for x in range(1, TOWER_WIDTH + 1):
            pos = Pos(x, y)
            sym = occupied_rocks.get(pos, '.')
            for rock in shape.rocks:
                if pos == shape_pos + rock:
                    sym = '@'
                    break
            print(sym, end='')
        print('|')
    print(f'+{"-" * TOWER_WIDTH}+')



def part1(file):
    jets = open(file, 'r').read()
    jets = jets.rstrip('\n')
    no_jets = len(jets)
    no_shapes = len(SHAPES)
    time = 0
    no_shapes_landed = 0
    next_shape = 0
    next_jet = 0
    """
7|...@...|
6|..@@@..|
5|...@...|
4|.......|
3|.......|
2|.......|
1|..####.|
0+-------+
 012345678
"""
    occupied = set()
    occupied_rocks = {}
    max_height = 0
    while no_shapes_landed < 2022:
        shape = SHAPES[next_shape]
        next_shape = (next_shape + 1) % no_shapes
        shape_pos = Pos(3, max_height + 4)
        if debug:
            print()
            print(f"== {no_shapes_landed} == {jets[next_jet:(min(next_jet + 10, no_jets))]}")
            print_tower(shape, shape_pos, occupied_rocks)
        while True:
            jet_sym = jets[next_jet]
            next_jet = (next_jet + 1) % no_jets
            jet = LEFT if jet_sym == "<" else (RIGHT if jet_sym == ">" else 1/0)

            new_shape_pos = shape_pos + jet
            if (not is_occupied(new_shape_pos, shape, occupied)) and is_in_bounds(new_shape_pos, shape):
                shape_pos = new_shape_pos

            if debug and no_shapes_landed <= 2:
                print()
                print(f"-- {no_shapes_landed} {jet_sym * 3} --")
                print_tower(shape, shape_pos, occupied_rocks)

            new_shape_pos = shape_pos + DOWN
            if is_occupied(new_shape_pos, shape, occupied) or (not is_in_bounds(new_shape_pos, shape)):
                # shape has landed
                no_shapes_landed += 1
                for rock in shape.rocks:
                    occupied.add(shape_pos + rock)
                    occupied_rocks[shape_pos + rock] = chr(ord('A') + next_shape)
                max_height = max([p.y for p in occupied])
                if debug and no_shapes_landed <= 2:
                    print()
                    print(f"-- {no_shapes_landed} shape has landed, max_height={max_height} --")
                    print_tower(shape, shape_pos, occupied_rocks)
                break
            else:
                shape_pos = new_shape_pos
                if debug and no_shapes_landed <= 2:
                    print()
                    print(f"-- {no_shapes_landed} shape falls 1 unit --")
                    print_tower(shape, shape_pos, occupied_rocks)

    print(max_height)




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
