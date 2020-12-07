"""
Day 7
"""

from typing import Tuple


def parse_line(line: str) -> Tuple[str, dict]:
    line = line[:-2] # Remove line break and dot
    i = line.find("contain")
    key = line[:i].strip()
    if key[-1] == 's':
        key = key[:-1] # remove s from bag
    line = line[i + len("contain"):]
    content = {}
    bags = line.split(",")
    for bag in bags:
        bag = bag.strip()
        if bag == 'no other bags' or bag == 'no other bag':
            continue
        split_bag = bag.split()
        amount = int(split_bag[0])
        bag_type = ' '.join(split_bag[1:])
        if bag_type[-1] == 's':
            bag_type = bag_type[:-1] # remove s from bags
        content[bag_type] = amount
    return key, content


def read_input(path: str) -> dict:
    out = {}
    with open(path, "r") as file:
        line = file.readline()
        while line != '':
            key, content = parse_line(line)

            out[key] = {"content": content}
            line = file.readline()
    return out


def contains_shiny(start_key: str, bags: dict) -> bool:    
    queue = []
    queue.append(start_key)

    while len(queue) > 0:
        current = queue.pop(0)

        if "shiny" in bags[current].keys() and bags[current]["shiny"]:
            bags[start_key]["shiny"] = True
            return True

        for inner_bag in bags[current]["content"].keys():
            if inner_bag == 'shiny gold bag':
                bags[start_key]["shiny"] = True
                return True

            if "shiny" in bags[inner_bag].keys() and not bags[inner_bag]["shiny"]:
                continue

            queue.append(inner_bag)

    bags[start_key]["shiny"] = False
    return False


def solve(bags: dict) -> int:
    out = 0

    for current_bag in bags.keys():
        if contains_shiny(current_bag, bags):
            out += 1

    return out


def count(current: str, bags: dict) -> int:
    if len(bags[current]["content"]) == 0:
        return 1
    out = 1
    for innerbag in bags[current]["content"].keys():
        out += bags[current]["content"][innerbag] * count(innerbag, bags)
    return out
    


if __name__ == "__main__":
    # bags = read_input('/Users/danielgrittner/development/advent-of-code2020/day7/input.txt')
    # print(solve(bags))

    bags2 = read_input('/Users/danielgrittner/development/advent-of-code2020/day7/input.txt')
    print(count("shiny gold bag", bags2) - 1)
