from __future__ import annotations

import functools
import sys

import util
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin
import os
import re
import ast

do_debug = False


def debug(args):
    if do_debug:
        print(args)


def main(file):
    part1(file)
    part2(file)


def parse_line(line):
    m = ast.parse(line).body[0].value

    def parse(node):
        if node.__class__ == ast.List:
            return [parse(elt) for elt in node.elts]
        elif node.__class__ == int:
            return node
        else:
            return node.value

    return parse(m)


def compare(l1, l2, lev=0):
    debug(f"{'  ' * lev}compare {l1}, {l2}")
    if l1.__class__ == int and l2.__class__ == int:
        return util.signum(l1 - l2)
    elif l1.__class__ == list and l2.__class__ == list:
        for i in range(min(len(l1), len(l2))):
            res = compare(l1[i], l2[i], lev + 1)
            if res != 0:
                return res
        return util.signum(len(l1) - len(l2))
    elif l1.__class__ == int:
        return compare([l1], l2, lev+1)
    elif l2.__class__ == int:
        return compare(l1, [l2], lev+1)
    else:
        raise Exception("should not happen")


def part1(file):
    eof = False
    f = open(file, 'r')
    pairs = []
    while not eof:
        pairs.append((parse_line(f.readline()), parse_line(f.readline())))
        line = f.readline()
        eof = line == ""

    index_sum = 0
    for index, (l1, l2) in enumerate(pairs, 1):
        res = compare(l1, l2)
        if res < 0:
            index_sum += index
    print(index_sum)


def part2(file):
    packets = [parse_line(line) for line in read_file_lines(file) if line != ""]
    divider_packets = [[[2]], [[6]]]
    packets.extend(divider_packets)
    sorted_packets = sorted(packets, key=functools.cmp_to_key(compare))
    idx1 = sorted_packets.index(divider_packets[0]) + 1
    idx2 = sorted_packets.index(divider_packets[1]) + 1
    print(idx1 * idx2)


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
