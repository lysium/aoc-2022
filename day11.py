from __future__ import annotations
import sys
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin
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


def main(file):
    part1(file)
    part2(file)


def parse_operation(line):
    """line is like 'new = old * 19'; return corresponding operation"""
    l = len("new = ")
    arg1, op_sym, arg2 = line[l:].split(' ')
    op = operator.mul if op_sym == "*" else operator.add
    op_str = "multiply" if op_sym == "*" else "add"
    if arg1 == "old" and arg2 == "old":
        return Operation(lambda old: op(old, old), f"{op_str} both: " + line)
    elif arg1 == "old":
        arg2 = int(arg2)
        return Operation(lambda old: op(old, arg2), f"{op_str} {arg2}: " + line)
    elif arg2 == "old":  # ... actually never happens in input11.txt
        arg1 = int(arg1)
        return Operation(lambda old:op(arg1, old), f"arg {op_sym} old: " + line)
    else:
        raise Exception(f"cannot parse operation line {line}")


def debug(arg):
    if do_debug:
        print(arg)


def part1(file):
    monkeys = read_monkeys_from_file(file)
    counts = [0 for _ in monkeys]
    for round in range(20):
        for monkey in monkeys:
            debug(f"Monkey {monkey.name}:")
            for item in monkey.items:
                counts[int(monkey.name)] += 1
                debug(f"  Monkey inspects an item with a worry level of {item}.")
                new_item = monkey.op.do(item)
                debug(f"    Worry level is {monkey.op.descr} to {new_item}.")
                new_item = new_item // 3
                debug(f"    Monkey gets bored with item. Worry level is divided by 3 to {new_item}.")
                target_monkey = monkey.test.yes_monkey if new_item % monkey.test.test == 0 else monkey.test.no_monkey
                debug(f"    Item with worry level 500 is thrown to monkey {target_monkey}.")
                monkeys[target_monkey].items.append(new_item)
            monkey.items = []
        debug(f"After round {round}:")
        for monkey in monkeys:
            debug(f"  Monkey {monkey.name}: {monkey.items}")
            pass

    for monkey, count in enumerate(counts):
        debug(f"Monkey {monkey}: {count}")
        pass
    max_count = max(counts)
    counts.remove(max_count)
    max2_count = max(counts)
    print(max_count * max2_count)


def part2(file):
    monkeys = read_monkeys_from_file(file)

    max_div = 1
    for monkey in monkeys:
        max_div *= monkey.test.test

    counts = [0 for _ in monkeys]
    for round in range(1,10_000+1):
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

    max_count = max(counts)
    counts.remove(max_count)
    max2_count = max(counts)
    print(max_count * max2_count)


def read_monkeys_from_file(file):
    monkeys = []
    monkey = None
    for line in read_file_lines(file):
        if line.startswith("Monkey"):
            l = len("Monkey ")
            name = int(line[l:l + 1])
        elif line.startswith("  Starting items:"):
            l = len("  Starting items:")
            items = [int(i) for i in (line[l:]).split(", ")]
        elif line.startswith("  Operation: "):
            l = len("  Operation: ")
            operation = parse_operation(line[l:])
        elif line.startswith("  Test: "):
            l = len("  Test: divisible by ")
            test_int = int(line[l:])
        elif line.startswith("    If true:"):
            l = len("    If true: throw to monkey ")
            test_yes = int(line[l:])
        elif line.startswith("    If false:"):
            l = len("    If false: throw to monkey ")
            test_no = int(line[l:])
        elif line == "":
            test = Test(test_int, test_yes, test_no)
            monkey = Monkey(name, items, operation, test)
            # print(monkey)
            monkeys.append(monkey)
    test = Test(test_int, test_yes, test_no)
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