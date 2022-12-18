from __future__ import annotations

import functools
import math
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
    droplets=[]
    for line in read_file_lines(file):
        droplet = [int(n) for n in line.split(',')]
        droplets.append(tuple(droplet))
    debug(len(droplets))
    part1(droplets)
    part2(droplets)


def part1(droplets):

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


def part2(droplets):
    mins = [math.inf for _ in range(3)]
    maxs = [-math.inf for _ in range(3)]
    for dim in range(3):
        mins[dim] = min([d[dim] for d in droplets])-1
        maxs[dim] = max([d[dim] for d in droplets])+1
        debug(f"min{dim}: ({mins[dim], maxs[dim]})")
    droplets_lu = set()
    for droplet in droplets:
        droplets_lu.add(droplet)
    start_droplet = (mins[0], mins[1], mins[2])
    water = [start_droplet]
    is_water = {start_droplet}
    surface = 0
    while water:
        water_droplet = water.pop(0)
        for delta in [(-1,0,0), (1,0,0),
                      (0,1,0), (0,-1,0),
                      (0,0,1), (0,0,-1)]:
            neighbor = (water_droplet[0] + delta[0], water_droplet[1] + delta[1], water_droplet[2] + delta[2])
            is_already_water = neighbor in is_water
            is_in_bounds = check_if_in_bounds(neighbor, mins, maxs)

            if not is_already_water and is_in_bounds:
                if neighbor in droplets_lu:
                    debug(f"hit {neighbor} from {water_droplet} via {delta}")
                    surface += 1
                else:
                    water.append(neighbor)
                    is_water.add(neighbor)
    print(surface)


def check_if_in_bounds(voxel, mins, maxs):
    is_in_bounds = True
    for dim in range(3):
        if not (mins[dim] <= voxel[dim] <= maxs[dim]):
            is_in_bounds = False
            break
    return is_in_bounds


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
