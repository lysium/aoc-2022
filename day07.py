import sys
from util import read_file_lines
from dataclasses import dataclass


def main(file):
    root = Dir("/", [], [], None)
    cwd = root
    for line in read_file_lines(file):
        if line.startswith("$"):
            cwd = handle_cmd(line, root, cwd)
        else:  # ls output
            if line.startswith("dir"):
                _, dir_name = line.split(' ')
                new_cwd = Dir(dir_name, [], [], cwd)
                cwd.dirs.append(new_cwd)
            else:
                size, file_name = line.split(' ')
                cwd.files.append(File(file_name, int(size)))
    print(result1(root.dirs))
    disk_size = 70000000
    needed_size = 30000000
    usage = root.size()
    free = disk_size - usage
    needed = needed_size - free
    candidate_dirs = result2(root.dirs, needed)
    min_sorted_dirs = sorted(candidate_dirs, key=lambda cd: cd[1])[0]
    print(min_sorted_dirs)


def handle_cmd(line, root, cwd):
    cmd_arg = line.split(' ')
    if cmd_arg[1] == "ls":
        pass  # implicitly ls output
    elif cmd_arg[1] == "cd":
        cwd = do_cwd(root, cwd, cmd_arg)
    return cwd


def do_cwd(root, cwd, cmd_arg):
    arg = cmd_arg[2]
    if arg == "/":
        cwd = root
    elif arg == "..":
        cwd = cwd.parent
    else:
        new_cwd = cwd.cd(arg)
        if new_cwd:
            cwd = new_cwd
        else:
            new_cwd = Dir(arg, [], [], cwd)
            cwd = new_cwd  # or new_cwd.cd(arg) for testing
    return cwd


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


def result2(dirs, needed):
    candidate_dirs = []
    for dir in dirs:
        dir_size = dir.size()
        if dir_size >= needed:
            candidate_dirs.append((dir.name, dir_size))
        candidate_dirs.extend(result2(dir.dirs, needed))
    return candidate_dirs


def result1(dirs):
    dir_sizes = 0
    for dir in dirs:
        dir_size = dir.size()
        if dir_size <= 100000:
            dir_sizes += dir_size
    return dir_sizes + sum([result1(dir.dirs) for dir in dirs])


if __name__ == "__main__":
    day = 7
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)