"""
Day 5
"""
import sys


def read_input(path: str) -> list:
    out = []
    with open(path, 'r') as file:
        line = file.readline()
        while line != '':
            out.append(line[:-1])  # Remove line break
            line = file.readline()
    return out


def compute_seat_id(seating_encoding: str) -> int:
    col_enc = seating_encoding[-3:]
    row_enc = seating_encoding[:-3]

    row_lower = 0
    row_upper = 127
    for c in row_enc:
        m = row_lower + ((row_upper - row_lower + 1) / 2)
        if c == 'F':
            # We keep the lower half
            row_upper = m - 1
        else:  # c == 'B'
            row_lower = m
    if row_lower != row_upper:
        raise ValueError(f'Fuck! lower={row_lower}, upper={row_upper}')
    row = row_lower

    col_lower = 0
    col_upper = 7
    for c in col_enc:
        m = col_lower + ((col_upper - col_lower + 1) / 2)
        if c == 'L':
            # We keep the lower half
            col_upper = m - 1
        else:
            # We keep the upper half
            col_lower = m
    if col_lower != col_upper:
        raise ValueError(f'Shit! lower={col_lower} upper={col_upper}')
    col = col_lower

    return row * 8 + col


def solve(input: list) -> int:
    highest_seat_id = -1
    for seating in input:
        seat_id = compute_seat_id(seating)
        if seat_id > highest_seat_id:
            highest_seat_id = seat_id
    return highest_seat_id


def solve2(input: list) -> int:
    highest_seat_id = -1
    lowest_seat_id = float('inf')
    seat_ids = []
    for seating in input:
        seat_id = compute_seat_id(seating)
        seat_ids.append(int(seat_id))
        if seat_id > highest_seat_id:
            highest_seat_id = seat_id
        if seat_id < lowest_seat_id:
            lowest_seat_id = seat_id
    seat_ids_set = set(seat_ids)

    print(f'highest={highest_seat_id}, lowest={lowest_seat_id}')  # FIXME:
    for seat_id in range(int(lowest_seat_id) + 1, int(highest_seat_id) - 1):
        if seat_id not in seat_ids_set:
            return seat_id

    return None



if __name__ == '__main__':
    input = read_input('/Users/danielgrittner/development/advent-of-code2020/day5/input.txt')
    # print(solve(input))
    # print(compute_seat_id('FBFBBFFRLR'))
    print(solve2(input))
