"""
Day 2
"""

def parse_line(line: str) -> dict:
    # Parse range
    out = {}
    index = 0
    # Parse min appearance
    while index < len(line):
        if line[index] == '-':
            out['min'] = int(line[:index])
            line = line[index + 1:]
            break
        index += 1
    # Parse max appearance
    index = 0
    while index < len(line):
        if line[index] == ' ':
            out['max'] = int(line[:index])
            line = line[index:]
            break
        index += 1
    # Parse char
    line = line[1:]
    out['char'] = line[0]
    # Parse password
    out['password'] = line[3:]
    return out


def read_input(path: str) -> list:
    out = []
    with open(path, 'r') as file:
        line = file.readline()
        while line != '':
            out.append(parse_line(line))
            line = file.readline()
    return out


def check_password(pw_config: dict) -> bool:
    count = {}
    for c in pw_config['password']:
        if c not in count.keys():
            count[c] = 1
        else:
            count[c] += 1

    if pw_config['char'] not in count.keys():
        return False

    return pw_config['min'] <= count[pw_config['char']] and count[pw_config['char']] <= pw_config['max']


def solve(input: list):
    valid = 0
    for pw_config in input:
        if check_password(pw_config):
            valid += 1
    return valid


def check_password2(pw_config: dict) -> bool:
    index1 = pw_config['min'] - 1
    is_first_set = pw_config['password'][index1] == pw_config['char']
    index2 = pw_config['max'] - 1
    is_second_set = pw_config['password'][index2] == pw_config['char']
    out = (is_first_set and not is_second_set) or (not is_first_set and is_second_set)
    print(f'pw={pw_config["password"]}, index1={index1}, index2={index2}')
    print(f'c={pw_config["char"]} min={pw_config["password"][index1]} max={pw_config["password"][index2]} => {out}')
    return out

def solve2(input: list):
    valid = 0
    for pw_config in input:
        if check_password2(pw_config):
            valid += 1
    return valid


if __name__ == "__main__":
    input = read_input('/Users/danielgrittner/development/advent-of-code2020/day2/input.txt')
    print(solve(input))

    input2 = read_input('/Users/danielgrittner/development/advent-of-code2020/day2/input2.txt')
    print(solve2(input2))
