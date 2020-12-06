"""
Day 6
"""

def read_input(path: str) -> list:
    out = []
    with open(path, 'r') as file_handle:
        group = []
        line = file_handle.readline()
        while line != '':
            if line == '\n':
                out.append(group)
                group = []
            else:
                group.append(line[:-1])
            line = file_handle.readline()

        if len(group) > 0:
            out.append(group)
    
    return out


def create_yes_count(group: list) -> dict:
    yes_answers = {}
    for answers in group:
        for answer in answers:
            if answer in yes_answers.keys():
                yes_answers[answer] += 1
            else:
                yes_answers[answer] = 1
    return yes_answers


def solve(groups: list) -> int:
    out = 0

    for group in groups:
        yes_answers = create_yes_count(group)
        out += len(yes_answers.keys())

    return out


def solve2(groups: list) -> int:
    out = 0

    for group in groups:
        group_members = len(group)
        yes_answers = create_yes_count(group)
        for question in yes_answers.keys():
            if yes_answers[question] == group_members:
                out += 1

    return out


if __name__ == "__main__":
    input = read_input('/Users/danielgrittner/development/advent-of-code2020/day6/input.txt')
    print(solve(input))
    print(solve2(input))
