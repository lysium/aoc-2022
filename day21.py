from __future__ import annotations

import operator
import sys
from util import read_file_lines
from dataclasses import dataclass
import os
import re

do_debug = False

def debug(args=None, end='\n'):
    if do_debug:
        print(args, end=end)


@dataclass(frozen=True)
class Monkey:
    name:str

@dataclass(frozen=True)
class MonkeyConst(Monkey):
    const:int

@dataclass(frozen=True)
class MonkeyOp(Monkey):
    op: str
    operands: [str]


def calculate_result(monkeys, results_cache, monkey_name):
    if monkey_name in results_cache:
        return results_cache[monkey_name]
    else:
        monkey = monkeys[monkey_name]
        if isinstance(monkey, MonkeyConst):
            results_cache[monkey] = monkey.const
            return results_cache[monkey]
        elif isinstance(monkey, MonkeyOp):
            op1, op2 = [calculate_result(monkeys, results_cache, op) for op in monkey.operands]
            if monkey.op == "*":
                op = operator.mul
            elif monkey.op == "/":
                op = operator.truediv
            elif monkey.op == "+":
                op = operator.add
            elif monkey.op == "-":
                op = operator.sub
            else:
                raise Exception(f"unknown operator in {monkey_name}")
            result = op(op1, op2)
            results_cache[monkey_name] = result
            return result

def main(file):
    pattern = "(\w\w\w\w): (\d+|(\w\w\w\w) ([-+*/]) (\w\w\w\w))"
    monkeys = {}
    for line in read_file_lines(file):
        m = re.search(pattern, line)
        if m:
            debug(f'{line}:\n    {[g for g in m.groups()]}')
            name = m.group(1)
            if m.group(5) is not None:
                monkey1, op, monkey2 = m.group(3), m.group(4), m.group(5)
                monkey = MonkeyOp(name, op, [monkey1, monkey2])
            else:
                const = int(m.group(2))
                monkey = MonkeyConst(name, const)
            monkeys[name] = monkey
        else:
            debug(f'{line}: NO MATCH')
    results_cache = dict([(monkey.name, monkey.const) for monkey in monkeys.values() if isinstance(monkey, MonkeyConst)])
    calculate_result(monkeys, results_cache, 'root')
    print(results_cache['root'])
    # part 2
    root_monkey = monkeys['root']
    left, right = root_monkey.operands
    if contains(monkeys, left, "humn"):
        human_tree = left
        expected = right
    else:
        human_tree = right
        expected = left
    expected_result = results_cache[expected]
    debug(f'expected result: {expected_result}')
    result = calculate_humn_result(monkeys, results_cache, human_tree, expected_result)
    print(f'humn yells {result}')


def contains(monkeys, tree_starting_at_name, monkey_name):
    if tree_starting_at_name == monkey_name: # shortcut
        return True
    monkey = monkeys[tree_starting_at_name]
    if isinstance(monkey, MonkeyConst):
        return monkey.name == monkey_name
    elif isinstance(monkey, MonkeyOp):
        return any([contains(monkeys, operand, monkey_name) for operand in monkey.operands])

def calculate_humn_result(monkeys, results_cache, monkey_name, expected_result):
    monkey = monkeys[monkey_name]
    if isinstance(monkey, MonkeyConst):
        if monkey_name == "humn":
            return expected_result
        else:
            return False
    elif isinstance(monkey, MonkeyOp):
        left, right = monkey.operands
        # first, suppose humn is left:
        right_result = results_cache[right]
        new_expected_result = None
        if monkey.op == '+':
            # x + right = expected -> x = expected - right
            new_expected_result = expected_result - right_result
        elif monkey.op == '-':
            # x - right = expected -> x = expected + right
            new_expected_result = expected_result + right_result
        elif monkey.op == '*':
            # x * right = expceted -> x = expcted / right
            new_expected_result = expected_result / right_result
        elif monkey.op == '/':
            # x / right = expected -> x = expected * right
            new_expected_result = expected_result * right_result
        result_if_humn_is_left = calculate_humn_result(monkeys, results_cache, left, new_expected_result)
        if result_if_humn_is_left:
            return result_if_humn_is_left
        else:
            # ok, humn wasn't left, so let's suppose humn is right:
            left_result = results_cache[left]
            if monkey.op == '+':
                # left + x = expected -> x = expected - left
                new_expected_result = expected_result - left_result
            elif monkey.op == '-':
                # left - x = expected -> x = left - expected
                new_expected_result = left_result - expected_result
            elif monkey.op == '*':
                # left * x = expceted -> x = expcted / left
                new_expected_result = expected_result / left_result
            elif monkey.op == '/':
                # left / x = expected -> x = left / expected
                new_expected_result = left_result / expected_result
            result_if_humn_is_right = calculate_humn_result(monkeys, results_cache, right, new_expected_result)
            if result_if_humn_is_right:
                return result_if_humn_is_right
            else:
                # humn was neither left nor right:
                return False


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
