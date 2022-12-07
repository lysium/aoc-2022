import sys
from util import read_file_lines
from dataclasses import dataclass


def main(file):
    part1(file)
    part2(file)


class Dir:
    def __init__(self, name, files, dirs, parent):
        self.name = name       # str
        self.files = files     # [str]
        self.dirs = dirs       # [Dir]
        self.parent = parent   # Dir

    def cd(self, dir_name):
        search = [dir for dir in self.dirs if dir.name == dir_name]
        if len(search) == 0:
            return None
        if len(search) > 1:
            raise Exception(f"many directories: {dir_name}")
        return search[0]

    def size(self):
        file_sizes = sum([file.size for file in self.files])
        dir_sizes = sum([dir.size() for dir in self.dirs if dir])
        return file_sizes + dir_sizes


@dataclass
class File:
    name: str
    size: int


def part1(file):
    """
    $ cd /
$ ls
dir bzgf
199775 dngdnvv.qdf
dir fhhwv
dir gzlpvdhd
dir htczftcn
"""
    fs = Dir("/", [], [], None)
    cwd = fs
    for line in read_file_lines(file):
        if line.startswith("$"):
            cmd_arg = line.split(' ')
            if cmd_arg[1] == "ls":
                pass  # implicitly ls output
            elif cmd_arg[1] == "cd":
                arg = cmd_arg[2]
                if arg == "/":
                    cwd = fs
                elif arg == "..":
                    cwd = cwd.parent
                else:
                    new_cwd = cwd.cd(arg)
                    if new_cwd:
                        cwd = new_cwd
                    else:
                        new_cwd = Dir(arg, [], [], cwd)
                        cwd = new_cwd   # or new_cwd.cd(arg) for testing
        else:        # ls output
            if line.startswith("dir"):
                _, dir_name = line.split(' ')
                new_cwd = Dir(dir_name, [], [], cwd)
                cwd.dirs.append(new_cwd)
            else:
                size, file_name = line.split(' ')
                cwd.files.append(File(file_name, int(size)))
    print(result1(fs.dirs))


def result1(dirs):
    dir_sizes = 0
    for dir in dirs:
        dir_size = dir.size()
        if dir_size <= 100000:
            dir_sizes += dir_size
    return dir_sizes + sum([result1(dir.dirs) for dir in dirs])



def part2(file):
    for line in read_file_lines(file):
        pass


if __name__ == "__main__":
    day = 7
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
