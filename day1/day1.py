"""
Day 1: Advent of Code
"""


def read_input(path: str) -> list:
    out = []
    with open(path, 'r') as file:
        line = file.readline()
        while line != '':
            out.append(int(line))
            line = file.readline()
    return out


def solve_for_two(input: list) -> int:
    my_set = set()
    for val in input:
        partner = 2020 - val

        if partner in my_set:
            return partner * val
        my_set.add(val)
    return -1


def solve_for_three(input: list) -> int:
    # TODO:
    available_nums = set(input)
    processed = set()

    for i in range(len(input)):
        for j in range(i + 1, len(input)):
            val1 = input[i]
            val2 = input[j]

            missing = 2020 - val1 - val2

            if missing in available_nums:
                return missing * val1 * val2

    return -1


if __name__ == '__main__':
    path = '/Users/danielgrittner/development/advent-of-code2020/day1/input.txt'
    input = read_input(path)
    print(solve_for_two(input))
    
    path2 = '/Users/danielgrittner/development/advent-of-code2020/day1/input2.txt'
    input2 = read_input(path2)
    print(solve_for_three(input2))
