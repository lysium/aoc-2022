from __future__ import annotations
import sys
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin


def main(file):
    part1(file)
    part2(file)


@dataclass
class Forest:
    trees: [int]
    width: int
    height: int


def is_visible(forest, x, y, dx, dy):
    tree = forest.trees[y][x]
    x += dx
    y += dy
    while (0 <= x < forest.width) and (0 <= y < forest.height):
        tree2 = forest.trees[y][x]
        if tree2 >= tree:
            return False
        else:
            pass
        x += dx
        y += dy
    return True


def viewing_distance(forest, x, y, dx, dy):
    tree = forest.trees[y][x]
    x += dx
    y += dy
    distance = 0
    while (0 <= x < forest.width) and (0 <= y < forest.height):
        distance += 1
        tree2 = forest.trees[y][x]
        if tree2 >= tree:
            break
        x += dx
        y += dy
    return distance


def part1(file):
    forest = []
    width = None
    for line in read_file_lines(file):
        forest_row = [int(tree) for tree in line]
        if width:
            assert(len(forest_row) == width)
        else:
            width = len(forest_row)
        forest.append(forest_row)
    height = len(forest)
    forest = Forest(forest, width, height)

    # naive
    count = 0
    for x in range(width):
        for y in range(height):
            if is_visible(forest, x, y, 0, 1) or \
                    is_visible(forest, x, y, 0, -1) or \
                    is_visible(forest, x, y, 1, 0) or \
                    is_visible(forest, x, y, -1, 0):
                count += 1
    print(count)

    max_scenic = 0
    for x in range(width):
        for y in range(height):
            scenic_score = viewing_distance(forest, x, y, 0, 1) * viewing_distance(forest, x, y, 0, -1) * viewing_distance(forest, x, y, 1, 0) * viewing_distance(forest, x, y, -1, 0)
            max_scenic = max(max_scenic, scenic_score)
    print(max_scenic)



def part2(file):
    for line in read_file_lines(file):
        pass


if __name__ == "__main__":
    day = 8
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
