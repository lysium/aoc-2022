from __future__ import annotations
import sys
from dataclasses import dataclass
import os
import re
import operator


do_debug = False


@dataclass
class Monkey:
    name: int
    items: [int]
    op: Operation
    test: Test

    def __repr__(self):
        return f"Monkey {self.name}: {self.items}, {self.op}, {self.test}"


@dataclass
class Operation:
    do: any  # (int) -> int
    descr: str

    def __repr__(self):
        return f"Op[{self.descr}]"


@dataclass
class Test:
    test: int  # divisible by ...
    yes_monkey: int
    no_monkey: int

    def __repr__(self):
        return f"Test[{self.test} ? {self.yes_monkey} : {self.no_monkey}]"

    @staticmethod
    def from_lines(test_l, test_no_l, test_yes_l):
        pattern = "(\d+)"
        test_int = int(re.search(pattern, test_l).group(1))
        test_yes = int(re.search(pattern, test_yes_l).group(1))
        test_no = int(re.search(pattern, test_no_l).group(1))
        test = Test(test_int, test_yes, test_no)
        return test


def main(file):
    part1(file)
    part2(file)


def parse_operation(line):
    """line is like '  Operation: new = old * 19'; return corresponding operation"""
    offset = len("  Operation: new = ")
    arg1, op_sym, arg2 = line[offset:].split(' ')
    op = operator.mul if op_sym == "*" else operator.add
    op_str = "multiply" if op_sym == "*" else "add"
    if arg1 == "old" and arg2 == "old":
        return Operation(lambda old: op(old, old), f"{op_str} both")
    elif arg1 == "old":
        arg2 = int(arg2)
        return Operation(lambda old: op(old, arg2), f"{op_str} {arg2}")
    elif arg2 == "old":  # ... actually never happens in input11.txt
        arg1 = int(arg1)
        return Operation(lambda old: op(arg1, old), f"arg {op_sym} old")
    else:
        raise Exception(f"cannot parse operation line {line}")


def debug(arg):
    if do_debug:
        print(arg)


def max2(counts):
    return sorted(counts, reverse=True)[0:2]


def part1(file):
    monkeys = read_monkeys_from_file(file)
    counts = [0 for _ in monkeys]
    for round in range(20):
        for monkey in monkeys:
            for item in monkey.items:
                counts[int(monkey.name)] += 1
                new_item = monkey.op.do(item)
                new_item = new_item // 3
                target_monkey = monkey.test.yes_monkey if new_item % monkey.test.test == 0 else monkey.test.no_monkey
                monkeys[target_monkey].items.append(new_item)
            monkey.items = []
    max1_count, max2_count = max2(counts)
    print(max1_count * max2_count)


def part2(file):
    monkeys = read_monkeys_from_file(file)

    max_div = 1
    for monkey in monkeys:
        max_div *= monkey.test.test

    counts = [0 for _ in monkeys]
    for round in range(1, 10_000+1):
        for monkey in monkeys:
            for item in monkey.items:
                counts[int(monkey.name)] += 1
                new_item = monkey.op.do(item)
                new_item = new_item % max_div
                target_monkey = monkey.test.yes_monkey if new_item % monkey.test.test == 0 else monkey.test.no_monkey
                monkeys[target_monkey].items.append(new_item)
                if target_monkey == int(monkey.name):
                    raise "Self-referrential"
            monkey.items = []
        if round == 1 or round == 20 or round % 1_000 == 0:
            debug(f"== After round {round} ==")
            for monkey, count in enumerate(counts):
                debug(f"Monkey {monkey}: {count}")

    max1_count, max2_count = max2(counts)
    print(max1_count * max2_count)


def read_monkeys_from_file(file):
    monkeys = []
    for monkey_lines in open(file, 'r').read().split('\n\n'):
        [monkey_l, items_l, op_line, test_l, test_yes_l, test_no_l] = monkey_lines.split('\n')[0:6]

        name = int(monkey_l[-2:-1])

        offset = len("  Starting items:")
        items = [int(i) for i in (items_l[offset:]).split(", ")]

        operation = parse_operation(op_line)
        test = Test.from_lines(test_l, test_no_l, test_yes_l)
        monkey = Monkey(name, items, operation, test)
        # print(monkey)
        monkeys.append(monkey)
    return monkeys


if __name__ == "__main__":
    this_script_name = os.path.basename(sys.argv[0])
    m = re.search('(\\d+)\\.py', this_script_name)
    if len(sys.argv) <= 1 and m:
        day = int(m.group(1))
        input_file = f"input{day:02}.txt"
    else:
        input_file = sys.argv[1]

    main(input_file)
