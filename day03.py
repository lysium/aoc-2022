import sys
from util import read_file_lines


def item_priority(item):
    if item.isupper():
        return ord(item) - ord('A') + 27
    else:
        return ord(item) - ord('a') + 1


def main(file):
    part1(file)
    part2(file)


def part2(file):
    total_badge_prio = 0
    group_items = []
    for line in read_file_lines(file):
        group_items.append(set(line))
        if len(group_items) == 3:
            badge_item = group_items[0].intersection(group_items[1]).intersection(group_items[2])
            if len(badge_item) > 1:
                raise "too many common items"
            badge_item_prio = item_priority(badge_item.pop())
            total_badge_prio += badge_item_prio
            group_items = []

    print(total_badge_prio)


def part1(file):
    total_prio = 0
    for line in read_file_lines(file):
        no_items = len(line)
        compartment1, compartment2 = line[0:no_items // 2], line[no_items // 2:]
        items1 = set(compartment1)
        items2 = set(compartment2)
        common_items = items1.intersection(items2)
        if len(common_items) > 1:
            raise "Too many common items"
        common_item = common_items.pop()
        common_item_prio = item_priority(common_item)
        total_prio += common_item_prio
    print(total_prio)


if __name__ == "__main__":
    input_file = "input03.txt" if len(sys.argv) <= 1 else sys.argv[1]
    main(input_file)
