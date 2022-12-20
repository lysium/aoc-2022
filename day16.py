from __future__ import annotations
import sys
from util import read_file_lines
from dataclasses import dataclass
from anytree import NodeMixin
import os
import re


def main(file):
    part1(file)
    part2(file)

@dataclass(frozen=True)
class Valve:
    id: str
    rate: int
    tunnels_to: [str]

@dataclass(frozen=True)
class Action:
    pass

@dataclass(frozen=True)
class OpenValve(Action):
    pass

@dataclass(frozen=True)
class MoveTo(Action):
    valve: str


def play(valve, valves, actions):
    total_pressure = 0
    current_pressure = 0
    minute = 1
    open_valves = set()
    actions = actions.copy()
    while True:
        total_pressure += current_pressure
        print(f'== Minute {minute} ==')
        if open_valves:
            print(f'Open valves: {", ".join(open_valves)}', end=', ')
            print(f' releasing {current_pressure} pressure (=? {sum([valves[v].rate for v in open_valves])})')
        else:
            print('No valves are open.')

        if minute > 30:
            break
        if actions:
            action = actions.pop(0)
            if isinstance(action, OpenValve):
                open_valves.add(valve)
                current_pressure += valves[valve].rate
            elif isinstance(action, MoveTo):
                valve = action.valve
            else:
                raise Exception(f"unknown action {action}")
        minute += 1
    return total_pressure

@dataclass()
class Trait:
    actions: [Action]
    valve: Valve
    open_valves: set(Valve)


def part1(file):
    pattern = 'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)'
    valves = {}
    for line in read_file_lines(file):
        m = re.search(pattern, line)
        if m:
            id = m.group(1)
            rate = int(m.group(2))
            tunnels_to = m.group(3).split(', ')
            valve = Valve(id, rate, tunnels_to)
            valves[id] = valve
            print(valve)
        else:
            raise Exception(f'no match for "{line}"')
        pass
    valve = 'AA'
    traits = [Trait([MoveTo(v)], v, set()) for v in valves[valve].tunnels_to]
    while len(traits[0].actions) < 30:
        new_traits = []
        for trait in traits:
            valve = trait.valve
            if (not valve in trait.open_valves) and valves[valve].rate:
                action = OpenValve()
                open_valves = trait.open_valves.copy().add(trait.valve)
                actions = trait.actions.copy()
                actions.append(action)
                new_traits.append(Trait(actions, valve, open_valves))
            for tunnel in valves[valve].tunnels_to:
                action = MoveTo(tunnel)
                actions = trait.actions.copy()
                actions.append(action)
                new_traits.append(Trait(actions, valve, trait.open_valves))

        traits = new_traits
    print("Traits", len(traits))
    for trait in traits:
        print(trait)


    if False:
        actions = [
            MoveTo('ZG'),
            MoveTo('PH'),
            OpenValve()
        ]
        tp = play(valve, valves, actions)
        print(f"total pressure: {tp}")


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
