"""
Day 17
"""
from copy import deepcopy


def read_input(path: str) -> list:
  output = []
  with open(path, 'r') as file_handle:
    line = file_handle.readline()
    while line != '':
      line = line[:-1] if line[-1] == '\n' else line
      output.append(list(line))
      line = file_handle.readline()
  return output


def print_grid(grid: list) -> None:
  for dim in grid:
    print("\n")
    for row in dim:
      print("".join(row))


def count_active_neighborhood(grid: list, d: int, r: int, c: int) -> int:
  """
  TODO: the same pattern as with 4D could and should be applied, this is too lengthy D:
  """
  active_neighbors = 0

  # Go one dimension back
  if d - 1 > 0 and grid[d - 1][r][c] == '#':
    active_neighbors += 1

  if d - 1 > 0 and r - 1 > 0 and grid[d - 1][r - 1][c] == '#':
    active_neighbors += 1

  if d - 1 > 0 and r + 1 < len(grid[d]) and grid[d - 1][r + 1][c] == '#':
    active_neighbors += 1

  if d - 1 > 0 and c - 1 > 0 and grid[d - 1][r][c - 1] == '#':
    active_neighbors += 1

  if d - 1 > 0 and r - 1 > 0 and c - 1 > 0 and grid[d - 1][r - 1][c - 1] == '#':
    active_neighbors += 1

  if d - 1 > 0 and r + 1 < len(grid[d]) and c - 1 > 0 and grid[d - 1][r + 1][c - 1] == '#':
    active_neighbors += 1

  if d - 1 > 0 and c + 1 < len(grid[d][r]) and grid[d - 1][r][c + 1] == '#':
    active_neighbors += 1

  if d - 1 > 0 and r - 1 > 0 and c + 1 < len(grid[d][r]) and grid[d - 1][r - 1][c + 1] == '#':
    active_neighbors += 1

  if d - 1 > 0 and r + 1 < len(grid[d]) and c + 1 < len(grid[d][r]) and grid[d - 1][r + 1][c + 1] == '#':
    active_neighbors += 1

  # Current dimension
  if r - 1 > 0 and grid[d][r - 1][c] == '#':
    active_neighbors += 1

  if r + 1 < len(grid[d]) and grid[d][r + 1][c] == '#':
    active_neighbors += 1

  if c - 1 > 0 and grid[d][r][c - 1] == '#':
    active_neighbors += 1

  if r - 1 > 0 and c - 1 > 0 and grid[d][r - 1][c - 1] == '#':
    active_neighbors += 1

  if r + 1 < len(grid[d]) and c - 1 > 0 and grid[d][r + 1][c - 1] == '#':
    active_neighbors += 1

  if c + 1 < len(grid[d][r]) and grid[d][r][c + 1] == '#':
    active_neighbors += 1

  if r - 1 > 0 and c + 1 < len(grid[d][r]) and grid[d][r - 1][c + 1] == '#':
    active_neighbors += 1

  if r + 1 < len(grid[d]) and c + 1 < len(grid[d][r]) and grid[d][r + 1][c + 1] == '#':
    active_neighbors += 1
  
  # Go one dimension further
  if d + 1 < len(grid) and grid[d + 1][r][c] == '#':
    active_neighbors += 1

  if d + 1 < len(grid) and r - 1 > 0 and grid[d + 1][r - 1][c] == '#':
    active_neighbors += 1

  if d + 1 < len(grid) and r + 1 < len(grid[d]) and grid[d + 1][r + 1][c] == '#':
    active_neighbors += 1

  if d + 1 < len(grid) and c - 1 > 0 and grid[d + 1][r][c - 1] == '#':
    active_neighbors += 1

  if d + 1 < len(grid) and r - 1 > 0 and c - 1 > 0 and grid[d + 1][r - 1][c - 1] == '#':
    active_neighbors += 1

  if d + 1 < len(grid) and r + 1 < len(grid[d]) and c - 1 > 0 and grid[d + 1][r + 1][c - 1] == '#':
    active_neighbors += 1

  if d + 1 < len(grid) and c + 1 < len(grid[d][r]) and grid[d + 1][r][c + 1] == '#':
    active_neighbors += 1

  if d + 1 < len(grid) and r - 1 > 0 and c + 1 < len(grid[d][r]) and grid[d + 1][r - 1][c + 1] == '#':
    active_neighbors += 1

  if d + 1 < len(grid) and r + 1 < len(grid[d]) and c + 1 < len(grid[d][r]) and grid[d + 1][r + 1][c + 1] == '#':
    active_neighbors += 1

  return active_neighbors


def next_cycle(grid: list) -> list:
  new_grid = deepcopy(grid)

  # Expand grid (naive solution)
  rows = len(new_grid[0])
  cols = len(new_grid[0][0])
  new_first_dim = [['.' for _ in range(cols)] for _ in range(rows)]

  new_grid.insert(0, deepcopy(new_first_dim))
  new_grid.append(deepcopy(new_first_dim))

  # We now need to add at every dimension a new bottom and top row
  new_row_blueprint = ['.' for _ in range(cols)]

  for dim in range(len(new_grid)):
    # Adapt new top and bottom row
    new_grid[dim].insert(0, new_row_blueprint.copy())
    new_grid[dim].append(new_row_blueprint.copy())
    # Adapt the sides
    for row in range(len(new_grid[dim])):
      new_grid[dim][row].insert(0, '.')
      new_grid[dim][row].append('.')

  # We deallocate grid since it is not needed anymore
  del grid

  # We now need to update the cubes of new grid as well
  new_active_positions = []
  new_inactive_positions = []
  
  for dim in range(len(new_grid)):
    for row in range(len(new_grid[dim])):
      for col in range(len(new_grid[dim][row])):
        active_neighborhood = count_active_neighborhood(new_grid, dim, row, col)
        if new_grid[dim][row][col] == '#' and not (2 <= active_neighborhood <= 3):
          new_inactive_positions.append((dim, row, col))
        elif new_grid[dim][row][col] == '.' and active_neighborhood == 3:
          new_active_positions.append((dim, row, col))

  # Update the positions we saved
  # Note: this way of computing results in a very bad cache behavior. :(
  for (d, r, c) in new_active_positions:
    new_grid[d][r][c] = '#'

  for (d, r, c) in new_inactive_positions:
    new_grid[d][r][c] = '.'

  return new_grid


def solve(dim: list, cycles: int = 6) -> int:
  grid = [dim]

  while cycles > 0:
    grid = next_cycle(grid)
    cycles -= 1

  # Count all active cubes in grid
  mapping= {'.': 0, '#': 1}
  return sum(map(lambda d: sum(map(lambda r: sum(map(lambda c: mapping[c], r)), d)), grid))


class Interval:
  def __init__(self, lower_bound: int, upper_bound: int):
    self.lower_bound = lower_bound
    self.upper_bound = upper_bound

  def __iter__(self) -> int:
    i = self.lower_bound
    while i <= self.upper_bound:
      yield i
      i += 1

  def contains(self, x: int) -> bool:
    return self.lower_bound <= x <= self.upper_bound

  def expand(self):
    self.lower_bound -= 1
    self.upper_bound += 1


def count_neighborhood4D_v2(grid: list, d1: int, d2: int, d3: int, d4: int, d1_inter: Interval, d2_inter: Interval, d3_inter: Interval, d4_inter: Interval) -> int:
  active_neighbors = 0

  for d1_ in range(d1 - 1, d1 + 2):
    for d2_ in range(d2 - 1, d2 + 2):
      for d3_ in range(d3 - 1, d3 + 2):
        for d4_ in range(d4 - 1, d4 + 2):
          if d1_ == d1 and d2_ == d2 and d3_ == d3 and d4_ == d4:
            continue
          if not d1_inter.contains(d1_) or not d2_inter.contains(d2_) or not d3_inter.contains(d3_) or not d4_inter.contains(d4_):
            continue

          key = (d1_, d2_, d3_, d4_)
          if key in grid.keys() and grid[key] == '#':
            active_neighbors += 1
  return active_neighbors


def next_cycle_v2(grid: dict, d1: Interval, d2: Interval, d3: Interval, d4: Interval) -> dict:
  new_active_positions = []
  new_inactive_positions = []

  for d1_ in d1:
    for d2_ in d2:
      for d3_ in d3:
        for d4_ in d4:
          active_neighborhood = count_neighborhood4D_v2(grid, d1_, d2_, d3_, d4_, d1, d2, d3, d4)
          key = (d1_, d2_, d3_, d4_)
          if key in grid.keys() and grid[key] == '#' and not (2 <= active_neighborhood <= 3):
            new_inactive_positions.append(key)
          elif (key not in grid.keys() or grid[key] == '.') and active_neighborhood == 3:
            new_active_positions.append(key)

  for key in new_active_positions:
    grid[key] = '#'

  for key in new_inactive_positions:
    grid[key] = '.'

  return grid


def print_grid_map(grid: dict, d1: Interval, d2: Interval, d3: Interval, d4: Interval) -> None:
  for d4_ in d4:
    for d3_ in d3:
      # Now print the d1 x d2 grid
      print(f'\nz = {d3_}, w = {d4_}')
      for d1_ in d1:
        row = ""
        for d2_ in d2:
          key = (d1_, d2_, d3_, d4_)
          if key in grid.keys():
            row += grid[key]
          else:
            row += "."
        print(row)


def solve2(dim: list, cycles: int = 6) -> int:
  grid = {}
  for row in range(len(dim)):
    for col in range(len(dim[row])):
      grid[(row, col, 0, 0)] = dim[row][col]

  d1 = Interval(0, len(dim) - 1)
  d2 = Interval(0, len(dim[0]) - 1)
  d3 = Interval(0, 0)
  d4 = Interval(0, 0)

  i = 1
  while cycles > 0:
    print(f'Cycle: {i}')
    d1.expand()
    d2.expand()
    d3.expand()
    d4.expand()
    
    grid = next_cycle_v2(grid, d1, d2, d3, d4)

    i += 1
    cycles -= 1

  # Count all active cubes in grid
  mapping= {'.': 0, '#': 1}
  return sum(map(lambda k: mapping[grid[k]], grid.keys()))


if __name__ == "__main__":
  dim = read_input("/Users/danielgrittner/development/advent-of-code2020/day17/input.txt")
  # print(solve(dim, cycles=6))
  print(solve2(dim, cycles=6))

