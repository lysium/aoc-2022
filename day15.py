from __future__ import annotations

import math
import sys

from pos import Pos
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin
import os
import re

from vec import Vec


def main(file):
    part1(file)
    part2(file)


@dataclass(repr=True, frozen=True)
class Sensor:
    pos: Pos
    beacon: Pos
    distance: int


def manhatten_distance(pos1, pos2):
    return abs(pos2.y - pos1.y) + abs(pos2.x - pos1.x)


def cut_y_line(pos, radius, line_y):
    """

    dy := abs(pos.y - line_y)
    left := pos.x - (radius-dy)
    right := pos.x + (radius+dy)

    d = 5
    dy = 3
    ....#####S####B...
    .....#.......#...
    ......#.....#....
    _______#####______

    d = 6
    dy= 3
    ...######S#####B..
    ....#.........#..
    .....#.......#...
    ______#######_____
    """
    dy = abs(pos.y - line_y)
    if dy > radius:
        return None, None
    left_x = pos.x - (radius - dy)
    right_x = pos.x + (radius - dy)
    return left_x, right_x


def part1(file):
    pattern = "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    sensors = []
    for line in read_file_lines(file):
        m = re.search(pattern, line)
        if m:
            sensor_x = int(m.group(1))
            sensor_y = int(m.group(2))
            beacon_x = int(m.group(3))
            beacon_y = int(m.group(4))
            sensor_pos = Pos(sensor_x, sensor_y)
            beacon_pos = Pos(beacon_x, beacon_y)
            sensor = Sensor(sensor_pos, beacon_pos, manhatten_distance(sensor_pos, beacon_pos))
            sensors.append(sensor)
        else:
            raise Exception("no match:" + line)
    print(len(sensors))
    min_x, min_y = math.inf, math.inf
    max_x, max_y = -math.inf, -math.inf
    for sensor in sensors:
        d = sensor.distance
        min_x, min_y = min(min_x, sensor.pos.x - d), min(min_y, sensor.pos.y - d)
        max_x, max_y = max(max_x, sensor.pos.x + d), max(max_y, sensor.pos.y + d)
    topleft = Pos(min_x, min_y)
    botright = Pos(max_x, max_y)
    print(min_x, max_x, (max_x - min_x))  # 6,323,285 points...

    no_beacon_pos = set()
    line_y = 2_000_000
    for sensor in sensors:
        left_x, right_x = cut_y_line(sensor.pos, sensor.distance, line_y)
        if left_x and right_x:
            no_beacon_pos.add(right_x)
            for left_x in range(left_x, right_x):
                no_beacon_pos.add(left_x)
    for sensor in sensors:
        if sensor.beacon.y == line_y and sensor.beacon.x in no_beacon_pos:
            no_beacon_pos.remove(sensor.beacon.x)
        if sensor.pos.y == line_y and sensor.beacon.x in no_beacon_pos:
            no_beacon_pos.remove(sensor.pos.x)
    print(len(no_beacon_pos))


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
