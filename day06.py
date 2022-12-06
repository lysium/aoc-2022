import sys
from util import read_file_lines


def main(file):
    execute(file, 4)
    execute(file, 14)


def all_different(buffer):
    seen = []
    for c in buffer:
        if c in seen:
            return False
        else:
            seen.append(c)
    return True


def execute(file, no_distinct):
    f = open(file, 'r')
    i = 1
    buffer = []
    while True:
        c = f.read(1)
        if c == '':
            raise Exception('nothing found')
        buffer.append(c)
        if len(buffer) == no_distinct:
            if all_different(buffer):
                print(i)
                return
            else:
                buffer = buffer[1:]
        i += 1


if __name__ == "__main__":
    day = 6
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
