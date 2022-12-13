from __future__ import annotations


def read_file_lines(file):
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            yield line


def signum(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
