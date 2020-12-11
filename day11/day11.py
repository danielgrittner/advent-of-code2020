"""
Day 11
"""
import copy


def read_input(path: str) -> list:
    out = []
    with open(path, "r") as file_handle:
        line = file_handle.readline()
        while line != '':
            line = line[:-1] if line[-1] == '\n' else line
            out.append(list(line))
            line = file_handle.readline()
    return out


def print_seats(seats: list) -> None:
    for row in seats:
        print(''.join(row))


def count_occupied_surrounding(seats: list, i: int, j: int) -> int:
    surrounding = 0

    # Upper-left
    if i > 0 and j > 0 and seats[i - 1][j - 1] == '#':
        surrounding += 1
    # Upper
    if i > 0 and seats[i - 1][j] == '#':
        surrounding += 1
    # Upper right
    if i > 0 and j < len(seats[i]) - 1 and seats[i - 1][j + 1] == '#':
        surrounding += 1
    # Left
    if j > 0 and seats[i][j - 1] == '#':
        surrounding += 1
    # Right
    if j < len(seats[i]) - 1 and seats[i][j + 1] == '#':
        surrounding += 1
    # Lower left
    if i < len(seats) - 1 and j > 0 and seats[i + 1][j - 1] == '#':
        surrounding += 1
    # Down
    if i < len(seats) - 1 and seats[i + 1][j] == '#':
        surrounding += 1
    # Lower right
    if i < len(seats) - 1 and j < len(seats[i]) - 1 and seats[i + 1][j + 1] == '#':
        surrounding += 1

    return surrounding


def count_running_surrounding(seats: list, i: int, j: int) -> int:
    surrounding = 0

    # Upper-left
    if i > 0 and j > 0:
        row = i - 1
        col = j - 1
        while row >= 0 and col >= 0 and seats[row][col] == '.':
            row -= 1
            col -= 1

        if row >= 0 and col >= 0 and seats[row][col] == '#':
            surrounding += 1
    
    # Upper
    if i > 0:
        row = i - 1
        while row >= 0 and seats[row][j] == '.':
            row -= 1

        if row >= 0 and seats[row][j] == '#':
            surrounding += 1

    # Upper right
    if i > 0 and j < len(seats[i]) - 1:
        row = i - 1
        col = j + 1
        while row >= 0 and col < len(seats[i]) and seats[row][col] == '.':
            row -= 1
            col += 1

        if row >= 0 and col < len(seats[i]) and seats[row][col] == '#':
            surrounding += 1

    # Left
    if j > 0:
        col = j - 1
        while col >= 0 and seats[i][col] == '.':
            col -= 1

        if col >= 0 and seats[i][col] == '#':
            surrounding += 1

    # Right
    if j < len(seats[i]) - 1:
        col = j + 1
        while col < len(seats[i]) and seats[i][col] == '.':
            col += 1

        if col < len(seats[i]) and seats[i][col] == '#':
            surrounding += 1

    # Lower left
    if i < len(seats) - 1 and j > 0:
        row = i + 1
        col = j - 1
        while row < len(seats) and col >= 0 and seats[row][col] == '.':
            row += 1
            col -= 1

        if row < len(seats) and col >= 0 and seats[row][col] == '#':
            surrounding += 1
    
    # Down
    if i < len(seats) - 1:
        row = i + 1
        while row < len(seats) and seats[row][j] == '.':
            row += 1

        if row < len(seats) and seats[row][j] and seats[row][j] == '#':
            surrounding += 1
        
    # Lower right
    if i < len(seats) - 1 and j < len(seats[i]) - 1:
        row = i + 1
        col = j + 1
        while row < len(seats) and col < len(seats[i]) and seats[row][col] == '.':
            row += 1
            col += 1
        
        if row < len(seats) and col < len(seats[i]) and seats[row][col] == '#':
            surrounding += 1

    return surrounding


def apply_rules_to_seats(seats: list, count_f=count_occupied_surrounding, threshold: int = 4) -> list:
    new_seats = copy.deepcopy(seats)

    for i in range(len(seats)):
        for j in range(len(seats[0])):
            if seats[i][j] == 'L':
                # Check adjacent seats
                surrounding = count_f(seats, i, j)
                if surrounding == 0:
                    # If no occupied seats adjacent are occupied, then, the seat becomes occupied
                    new_seats[i][j] = '#'
            elif seats[i][j] == '#':
                # Check adjacent seats
                surrounding = count_f(seats, i, j)
                if surrounding >= threshold:
                    # if four or more seats adjacent to the current seat are occupied, the seat becomes empty
                    new_seats[i][j] = 'L'

    return new_seats


def solve(seats: list, count_f=count_occupied_surrounding, threshold: int = 4) -> int:
    while True:
        new_seats = apply_rules_to_seats(seats, count_f, threshold=threshold)
        if new_seats == seats:
            # We reached convergence, hence, stop here
            new_seats = seats
            break
        seats = new_seats
    return sum(map(lambda row: len(list(filter(lambda pos: pos == '#', row))), seats))


if __name__ == "__main__":
    seats = read_input('/Users/danielgrittner/development/advent-of-code2020/day11/input.txt')
    print(solve(seats, count_running_surrounding, threshold=5))
