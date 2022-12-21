from __future__ import annotations

import operator
import sys
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin
import os
import re
from collections import deque, defaultdict

do_debug = False

def debug(args=None, end='\n'):
    if do_debug:
        print(args, end=end)

### adapted from https://algotree.org/algorithms/tree_graph_traversal/topological_sort/
class Graph :

    def __init__(self, nodes : [str]) :
        self.nodes = nodes
        self.visited = set()
        # The default dictionary would create an empty list as a default (value)
        # for the nonexistent keys.
        self.adjlist = defaultdict(list)
        self.stack  = deque()

    def AddEdge(self, src : str, dst : str) :
        self.adjlist[src].append(dst)

    def TopologicalSort(self, src : str) :

        self.visited.add(src)

        # Check if there is an outgoing edge for a node in the adjacency list
        for node in self.adjlist[src] :
            if not (node in self.visited):
                self.TopologicalSort(node)

        # Only after all the nodes on the outgoing edges are visited push the
        # source node in the stack
        self.stack.append(src)

    def Traverse(self, op) :
        has_edges = set(self.adjlist.keys())
        for node in set(self.nodes).difference(has_edges):
            if not (node in self.visited):
                self.TopologicalSort(node)
        for node in self.nodes:
            if not (node in self.visited):
               self.TopologicalSort(node)

        while self.stack :
            arg = self.stack.popleft()
            op(arg)


def main(file):
    part1(file)
    part2(file)


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


def test_topsort():
    g = Graph(sorted(['12', '13', '15', '+', '*', '/', '18']))
    g.AddEdge('+', '13')
    g.AddEdge('+', '13')
    g.AddEdge('*', '+')
    g.AddEdge('*', '12')
    g.AddEdge('/', '*')
    g.AddEdge('/', '18')
    result = []
    g.Traverse(lambda x: result.append(x))
    assert set(result[0:4]) == {'15', '12', '18', '13'}
    assert set(result[4:7]) == {'+', '*', '/'}

def part1(file):
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

    g = Graph(monkeys.keys())

    for monkey in monkeys.values():
        if isinstance(monkey, MonkeyOp):
            g.AddEdge(monkey.name, monkey.operands[0])
            g.AddEdge(monkey.name, monkey.operands[1])

    topsort = []
    g.Traverse(lambda name: topsort.append(name))
    results = dict([(monkey.name, monkey.const) for monkey in monkeys.values() if isinstance(monkey, MonkeyConst)])
    for key in results.keys():
        debug(f' -> {key}: {results[key]}', end=', ')
    debug()
    for name in topsort:
        monkey = monkeys[name]
        debug(f'-> {name}: {monkey}')
        if isinstance(monkey, MonkeyConst):
            results[name] = monkey.const
        elif isinstance(monkey, MonkeyOp):
            if monkey.op == "*":
                op = operator.mul
            elif monkey.op == "/":
                op = operator.truediv
            elif monkey.op == "+":
                op = operator.add
            elif monkey.op == "-":
                op = operator.sub
            else:
                raise Exception(f'unknown op {monkey.op} in {name}')
            operand1, operand2 = monkey.operands
            results[name] = op(results[operand1], results[operand2])

    print(results['root'])

    root = monkeys['root']
    left = root.operands[0]
    right = root.operands[1]
    if contains(monkeys, "humn", left):
        human_tree = left
        expected = right
    else:
        human_tree = right
        expected = left
    expected_result = results[expected]

    print(f'expected result: {expected_result}')
    result = part2x(human_tree, expected_result, monkeys, results)
    print(f'humn yells {result}')


def contains(monkeys, monkey_name, tree):
    if tree == monkey_name:
        return True
    monkey = monkeys[tree]
    if isinstance(monkey, MonkeyConst):
        return monkey.name == monkey_name
    elif isinstance(monkey, MonkeyOp):
        return contains(monkeys, monkey_name, monkey.operands[0]) or contains(monkeys, monkey_name, monkey.operands[1])

def part2x(node, expected_result, monkeys, results):
    monkey = monkeys[node]
    if isinstance(monkey, MonkeyConst):
        if node == "humn":
            return expected_result
        else:
            return False
    elif isinstance(monkey, MonkeyOp):
        left, right = monkey.operands
        # first, humn is left:
        right_result = results[right]
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
        test_left = part2x(left, new_expected_result, monkeys, results)
        if test_left:
            return test_left
        else:
            # then suppose humn is right:
            # elif right == "humn":
            left_result = results[left]
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
            test_right =  part2x(right, new_expected_result, monkeys, results)
            if test_right:
                return test_right
            else:
                return False


def part2(file):
    for line in read_file_lines(file):
        pass


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
