from __future__ import annotations
import sys
from util import read_file_lines
from dataclasses import dataclass
import os
import re
from pos import Pos
from vec import Vec, UP, DOWN, LEFT, RIGHT


def main(file):
    map = read_map_from_file(file)
    length = part1(map)
    print(length)
    length = part2(map)
    print(length)


@dataclass(frozen=True)
class Map:
    map: [str]
    dimension: Vec
    START = "S"
    END = "E"

    @staticmethod
    def create(map):
        return Map(map, Vec(len(map[0]), len(map)))

    def __getitem__(self, item):
        if item.__class__ == Pos:
            return self.map[item.y][item.x]
        else:
            return self.map[item]

    def altitude(self, pos):
        height = self[pos]
        if height == Map.START:
            height = 'a'
        elif height == Map.END:
            height = 'z'
        return ord(height) - ord('a')


def find_start(map):
    for y in range(map.dimension.dy):
        x = map[y].find(Map.START)
        if x != -1:
            return Pos(x, y)


def find_a(map):
    result = []
    for y in range(map.dimension.dy):
        for x, c in enumerate(map[y]):
            if c == 'a' or c == 'S':
                result.append(Pos(x, y))
    return result


def can_go(map, start, end):
    if 0 <= end.x < map.dimension.dx and 0 <= end.y < map.dimension.dy:
        start_altitude = map.altitude(start)
        end_altitude = map.altitude(end)
        return end_altitude - start_altitude <= 1
    else:
        return False


def part1(map):
    start = find_start(map)
    length = find_shortest_path(map, [start])
    return length


def part2(map):
    a_positions = find_a(map)
    length = find_shortest_path(map, a_positions)
    return length


def find_shortest_path(map, start_positions):
    trails = [[pos] for pos in start_positions]
    visited = set(start_positions)
    length = None
    while not length:
        new_trails = []
        for trail in trails:
            head = trail[-1]
            if map[head] == map.END:
                length = len(trail) - 1  # w/o START
                break
            for dir in [UP, DOWN, RIGHT, LEFT]:
                new_pos = head + dir
                if (not (new_pos in visited)) and can_go(map, head, new_pos):
                    new_trail = trail.copy()
                    new_trail.append(new_pos)
                    new_trails.append(new_trail)
                    visited.add(new_pos)
        trails = new_trails
    return length


def read_map_from_file(file):
    map = [line for line in read_file_lines(file)]
    return Map.create(map)


if __name__ == "__main__":
    this_script_name = os.path.basename(sys.argv[0])
    m = re.search('(\\d+)\\.py', this_script_name)
    if len(sys.argv) <= 1 and m:
        day = int(m.group(1))
        input_file = f"input{day:02}.txt"
    else:
        input_file = sys.argv[1]

    main(input_file)
