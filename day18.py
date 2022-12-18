from __future__ import annotations

import functools
import sys
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin
import os
import re


do_debug = False
def debug(args):
    if do_debug:
        print(args)


def main(file):
    part1(file)
    part2(file)


def part1(file):
    droplets=[]
    for line in read_file_lines(file):
        droplet = [int(n) for n in line.split(',')]
        droplets.append(droplet)
    debug(len(droplets))

    # group by x,y
    debug("== 0, 1 ==")
    neighbors01 = count_neighbors(droplets, 0, 1, 2)
    debug(f" >> {neighbors01} neighbors")
    debug("== 0, 2 ==")
    neighbors02 = count_neighbors(droplets, 0, 2, 1)
    debug(f" >> {neighbors02} neighbors")
    debug("== 1, 2 ==")
    neighbors12 = count_neighbors(droplets, 1, 2, 0)
    debug(f" >> {neighbors12} neighbors")
    neighbors = neighbors01 + neighbors02 + neighbors12
    print(len(droplets) * 6 - neighbors * 2)


def count_neighbors(droplets, dim1, dim2, dim3):
    dim12 = {}
    neighbors = 0
    for droplet in droplets:
        key = (droplet[dim1], droplet[dim2])
        dim12.setdefault(key, []).append(droplet[dim3])
    for dim12_key in sorted(dim12.keys()):
        dim3s = sorted(dim12[dim12_key])
        dim12[dim12_key] = dim3s
        last_dim3 = dim12[dim12_key][0]
        n = 0
        for this_dim3 in dim3s[1:]:
            if last_dim3 + 1 == this_dim3:
                n += 1
            last_dim3 = this_dim3
        debug(f"{dim12_key}: {dim3s}: {n} neighbors")
        neighbors += n
    return neighbors


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
