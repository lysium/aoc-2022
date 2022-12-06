import sys
from util import read_file_lines


def main(file):
    part1(file)
    part2(file)


def all_different(buffer):
    seen = []
    for c in buffer:
        if c in seen:
            return False
        else:
            seen.append(c)
    return True


def part1(file):
    f=open(file, 'r')
    i=1
    buffer=[]
    while True:
        c = f.read(1)
        if c == '':
           raise Exception('nothing found')
        buffer.append(c)
        print(buffer)
        if len(buffer) == 4:
            if all_different(buffer):
                print(i)
                return
            else:
                buffer = buffer[1:]
        i += 1


def part2(file):
    for line in read_file_lines(file):
        pass


if __name__ == "__main__":
    day = 6
    input_file = f"input{day:02}.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
