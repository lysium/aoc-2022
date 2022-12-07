from __future__ import annotations
import sys
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin


@dataclass
class File:
    name: str
    size: int


class Dir(NodeMixin):
    name: str
    files: [str]

    def __init__(self, name, files=None, parent=None, children=None):
        self.name = name
        self.files = files if files else []
        self.parent = parent
        if children:
            self.children = children

    def dirs(self):
        return self.children

    def cd(self, dir_name):
        search = [dir for dir in self.dirs() if dir.name == dir_name]
        if len(search) == 0:
            return None
        if len(search) > 1:
            raise Exception(f"many directories: {dir_name}")
        return search[0]

    def size(self):
        file_sizes = sum([file.size for file in self.files])
        dir_sizes = sum([dir.size() for dir in self.dirs() if dir])
        return file_sizes + dir_sizes

    def __repr__(self):
        return self.name


def main(file):
    root = read_dir_tree_from_file(file)
    part1(root)
    part2(root)


def part1(root):
    print(sum_dir_sizes_le_100_000(root.dirs()))


def part2(root):
    disk_size = 7_000_0000
    needed_size = 3_000_0000
    usage = root.size()
    free = disk_size - usage
    needed = needed_size - free
    candidate_dirs = find_dirs_lt(root.dirs(), needed)
    min_sorted_dirs = min(candidate_dirs, key=lambda cd: cd[1])
    print(min_sorted_dirs)


def read_dir_tree_from_file(file):
    root = Dir("/")
    cwd = root
    for line in read_file_lines(file):
        if line.startswith("$"):
            words = line.split(' ')  # 0:"$"
            cwd = handle_cmd(words[1:], root, cwd)
        else:  # we only have ls output
            if line.startswith("dir"):
                _, dir_name = line.split(' ')
                new_cwd = Dir(dir_name, parent=cwd)
            else:
                size, file_name = line.split(' ')
                cwd.files.append(File(file_name, int(size)))
    return root


def handle_cmd(words, root, cwd):
    cmd = words[0]
    if cmd == "ls":
        pass  # implicitly ls output
    elif cmd == "cd":
        cwd = do_cwd(root, cwd, words[1:])
    return cwd


def do_cwd(root, cwd, args):
    arg = args[0]
    if arg == "/":
        cwd = root
    elif arg == "..":
        cwd = cwd.parent
    else:
        maybe_dir = [c for c in cwd.dirs() if c.name == arg]
        if maybe_dir:
            cwd = maybe_dir[0]
        else:
            new_cwd = Dir(arg, parent=cwd)
            cwd = new_cwd
    return cwd


def find_dirs_lt(dirs, needed):
    candidate_dirs = []
    for dir in dirs:
        dir_size = dir.size()
        if dir_size >= needed:
            candidate_dirs.append((dir.name, dir_size))
        candidate_dirs.extend(find_dirs_lt(dir.dirs(), needed))
    return candidate_dirs


def sum_dir_sizes_le_100_000(dirs):
    dir_sizes = 0
    for dir in dirs:
        dir_size = dir.size()
        if dir_size <= 100_000:
            dir_sizes += dir_size
    return dir_sizes + sum([sum_dir_sizes_le_100_000(dir.dirs()) for dir in dirs])


if __name__ == "__main__":
    day = 7
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
