"""
Day 16
"""
from typing import Tuple
from copy import deepcopy
from functools import cmp_to_key


class Interval:
  def __init__(self, interval_str: str): 
    interval_split = interval_str.split('-')
    self.start = int(interval_split[0])
    self.end = int(interval_split[1])
    assert self.start <= self.end

  def contains(self, x: int) -> bool:
    return self.start <= x <= self.end


class Constraint:
  def __init__(self, constraint_str: str):
    constraint_split = constraint_str.split()

    # Find out constraint name
    i = 0
    while constraint_split[i][-1] != ':':
      i += 1
    self.name = (' '.join(constraint_split[:i + 1]))[:-1]  # Remove colon

    constraint_split = constraint_split[i + 1:]
    # Filter out 'or' and build intervals
    self.constraint_intervals = list(map(lambda x: Interval(x), filter(lambda x: x != 'or', constraint_split)))

    self.min = min(map(lambda interval: interval.start, self.constraint_intervals))
    self.max = max(map(lambda interval: interval.end, self.constraint_intervals))

  def matches_constraint(self, x: int) -> bool:
    return any(map(lambda interval: interval.contains(x), self.constraint_intervals))


def read_input(path: str) -> Tuple[list, list, list]:
  constraints = []
  my_ticket = []
  nearby_tickets = []
  
  parse_ticket = lambda ticket_str: list(map(lambda x: int(x), ticket_str.split(',')))
  
  with open(path, "r") as file_handle:
    # Parse contraints
    line = file_handle.readline()
    while line != '\n':
      constraints.append(Constraint(line))
      line = file_handle.readline()

    # Parse my ticket
    line = file_handle.readline()
    assert line == 'your ticket:\n'
    line = file_handle.readline()
    my_ticket = parse_ticket(line[:-1])

    line = file_handle.readline()  # Again an empty line

    # Parse nearby tickets
    line = file_handle.readline()
    assert line == 'nearby tickets:\n'
    line = file_handle.readline()
    while line != '':
      line = line[:-1] if line[-1] == '\n' else line
      nearby_tickets.append(parse_ticket(line))
      line = file_handle.readline()

  return constraints, my_ticket, nearby_tickets


def solve(constraints: list, nearby_tickets) -> int:
  error_rate = 0

  for ticket in nearby_tickets:
    for num in ticket:
      valid = False
      for constraint in constraints:
        if constraint.matches_constraint(num):
          valid = True
          break

      if not valid:
        error_rate += num

  return error_rate


def solve2(constraints: list, my_ticket: list, nearby_tickets: list) -> int:
  valid_tickets = [my_ticket]

  for ticket in nearby_tickets:
    ticket_valid = True
    for num in ticket:
      num_valid = False
      for constraint in constraints:
        if constraint.matches_constraint(num):
          num_valid = True
          break

      if not num_valid:
        ticket_valid = False
        break

    if ticket_valid:
      valid_tickets.append(ticket)

  # Find out constraint order
  constraint_order = [deepcopy(constraints) for _ in range(len(my_ticket))]

  # Now, we need to filter out the invalid constraints for a position
  for ticket in valid_tickets:
    for i in range(len(constraint_order)):
      constraint_order[i] = list(filter(lambda constraint: constraint.matches_constraint(ticket[i]), constraint_order[i]))
  
  cmp = lambda item1, item2: len(constraint_order[item1]) - len(constraint_order[item2])
  index_map = list(range(len(constraint_order)))
  index_map = sorted(index_map, key=cmp_to_key(cmp))
  
  # If there are multiple constraints for a position available, we remove the fixed constraints
  fixed_constraints = set()  # Fixed constraints are constraints which are the only ones left for a certain position
  for i in index_map:
    if len(constraint_order[i]) > 1:
      constraint_order[i] = list(filter(lambda c: c.name not in fixed_constraints, constraint_order[i]))
    assert len(constraint_order[i]) == 1
    constraint_order[i] = constraint_order[i][0]
    fixed_constraints.add(constraint_order[i].name)

  out = 1
  for i, constraint in enumerate(constraint_order):
    if "departure" in constraint.name:
      out *= my_ticket[i]

  return out


if __name__ == "__main__":
  # constraints, _, nearby_tickets = read_input('/Users/danielgrittner/development/advent-of-code2020/day16/input.txt')
  # print(solve(constraints, nearby_tickets))

  constraints, my_ticket, nearby_tickets = read_input('/Users/danielgrittner/development/advent-of-code2020/day16/input.txt')
  print(solve2(constraints, my_ticket, nearby_tickets))
