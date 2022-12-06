import sys
from enum import Enum
import timeit


def main(argv):
    day = 6
    input_file = f"input{day:02}.txt"
    method = Method.PLAIN
    times = 0
    if len(argv) >= 2:
        input_file = sys.argv[1]
    if len(argv) >= 3:
        method = Method(sys.argv[2])
    if len(argv) >= 4:
        times = int(sys.argv[3])

    if method == Method.PLAIN:
        execute = execute_plain
    elif method == Method.DICT:
        execute = execute_with_dict
    elif method == Method.LIST:
        execute = execute_with_list
    else:
        raise Exception("unknown method")

    print(execute(input_file, 4))
    print(execute(input_file, 14))

    if times > 0:
        duration = timeit.timeit(f'{execute.__name__}("{input_file}", 14)',
                                 setup=f"from __main__ import {execute.__name__}",
                                 number=times)
        print(f'duration: {duration}')
        print(f'duration/times: {duration/times}')


def all_different(buffer):
    seen = []
    for c in buffer:
        if c in seen:
            return False
        else:
            seen.append(c)
    return True


def execute_plain(file, no_distinct):
    f = open(file, 'r')
    no_chars = 1
    buffer = []
    while True:
        c = f.read(1)
        if c == '':
            raise Exception('nothing found')
        buffer.append(c)
        if len(buffer) == no_distinct:
            if all_different(buffer):
                return no_chars
            else:
                buffer = buffer[1:]
        no_chars += 1


def execute_with_dict(file, no_distinct):
    f = open(file, 'r')
    no_chars = 1
    buffer = []
    seen = {}
    while True:
        c = f.read(1)
        if c == '':
            raise Exception('nothing found')
        buffer.append(c)
        seen[c] = seen.setdefault(c, 0) + 1
        if len(buffer) == no_distinct:
            if all([count <= 1 for count in seen.values()]):
                return no_chars
            else:
                seen[buffer[0]] -= 1
                buffer = buffer[1:]
        no_chars += 1


def execute_with_list(file, no_distinct):
    f = open(file, 'r')
    no_chars = 1
    buffer = []
    ord_a = ord('a')
    seen = [0 for _ in range(ord('z') - ord_a + 1)]
    while True:
        c = f.read(1)
        if c == '':
            raise Exception('nothing found')
        buffer.append(c)
        seen[ord(c) - ord_a] += 1
        if len(buffer) == no_distinct:
            if all([count <= 1 for count in seen]):
                return no_chars
            else:
                seen[ord(buffer[0]) - ord_a] -= 1
                buffer = buffer[1:]
        no_chars += 1


class Method(Enum):
    PLAIN = "plain"
    DICT = "dict"
    LIST = "list"


if __name__ == "__main__":
    main(sys.argv)
