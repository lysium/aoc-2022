from __future__ import annotations
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
    print(part1(file))
    print(part2(file))


def part1(file):
    return decrypt(file, 1, 1)

def part2(file):
    return decrypt(file, 811589153, 10)

class Number:
    def __init__(self, n:int, prev:Number = None, next:Number = None):
        self.n = n
        self.prev = prev
        self.next = next

def remove(number:Number):
    number.prev.next = number.next
    number.next.prev = number.prev
    number.prev = None
    number.next = None

def insert_after(number:Number, where:Number):
    number.next = where.next
    number.prev = where
    where.next = number
    number.next.prev = number

def print_numbers(start:Number):
    print(start.n, end =', ')
    number = start.next
    while number != start:
        print(number.n, end=', ')
        number = number.next
    print()

def decrypt(file, decryption_key, rounds):
    numbers = [Number(int(line) * decryption_key) for line in read_file_lines(file)]
    length = len(numbers)
    for i in range(0, length):
        numbers[i].prev = numbers[i - 1]
        numbers[i].next = numbers[(i + 1) % length]

    for _ in range(rounds):
        for number in numbers:
            steps = number.n
            insert_here = number.prev
            remove(number)
            steps = steps % (length - 1)
            for i in range(steps):
                insert_here = insert_here.next
            insert_after(number, insert_here)

    zero = numbers[0]
    while zero.n != 0:
        zero = zero.next
    coordinates = []
    for _ in range(3):
        for _ in range(1000):
            zero = zero.next
        coordinates.append(zero.n)
    debug(coordinates)
    return sum(coordinates)


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
