"""
Day 3
"""


def read_input(path: str) -> list:
    out = []
    with open(path, 'r') as file:
        line = file.readline()
        while line != '':
            row = [c for c in line[:-1]]
            out.append(row)
            line = file.readline()
    return out


def solve(env: list, step_right: int, step_down: int = 1) -> int:
    trees = 0
    current_col = 0
    current_row = step_down

    number_of_cols = len(env[0])

    while current_row < len(env):
        current_col = (current_col + step_right) % number_of_cols
        if env[current_row][current_col] == '#':
            trees += 1
        current_row += step_down

    return trees


if __name__ == "__main__":
    input = read_input("/Users/danielgrittner/development/advent-of-code2020/day3/input.txt")
    # print(solve(input, 3))
    
    # Right 1, down 1
    first = solve(input, 1)
    # Right 3, down 1
    second = solve(input, 3)
    # Right 5, down 1
    third = solve(input, 5)
    # Right 7, down 1
    fourth = solve(input, 7)
    # Right 1, down 2
    fifth = solve(input, 1, step_down=2)

    print(first * second * third * fourth * fifth)

