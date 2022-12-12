from __future__ import annotations
import sys
from util import read_file_lines
from dataclasses import dataclass
import os
import re
from pos import Pos
from vec import Vec


def main(file):
    length = part1(file)
    print(length)
    part2(file)


@dataclass
class Map:
    map: [str]
    width: int
    height: int
    START = "S"
    END = "E"

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


UP = Vec(0, -1)
DOWN = Vec(0, 1)
LEFT = Vec(-1, 0)
RIGHT = Vec(1, 0)


def find_start(map):
    for y in range(map.height):
        x = map[y].find(Map.START)
        if x != -1:
            return Pos(x, y)


def can_go(map, start, end):
    if 0 <= end.x < map.width and 0 <= end.y < map.height:
        start_altitude = map.altitude(start)
        end_altitude = map.altitude(end)
        return end_altitude - start_altitude <= 1
    else:
        return False


def part1(file):
    map = read_map_from_file(file)

    start = find_start(map)
    length = find_shortest_path(map, start)
    return length


def find_shortest_path(map, start):
    trails = [[start]]
    visited = {start}
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
    map = []
    for line in read_file_lines(file):
        map.append(line)
    map = Map(map, len(map[0]), len(map))
    return map


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
