"""
Day 10
"""

def read_input(path: str) -> list:
  out = []
  with open(path, "r") as file_handle:
    line = file_handle.readline()
    while line != "":
      line = line[:-1] if line[-1] == '\n' else line
      out.append(int(line))
      line = file_handle.readline()
  return out


def solve(input: list) -> int:
  cnts = {
    1: 0,
    2: 0,
    3: 1  # Already 1 since the device and last adapter always have a difference of 3
  }
  last_jolt = 0
  input = sorted(input)
  for next in input:
    cnts[next - last_jolt] += 1
    last_jolt = next
  return cnts[1] * cnts[3]


def is_within_range(diff: int) -> bool:
  return 0 < diff <= 3


def solve2(input: list) -> int:
  input = sorted(input)
  print(input)
  jolt_own_device = input[-1] + 3

  memo = {}

  def compute_all_possible_adapter_combs(input: list, last_jolt: int, current_index: int, jolt_own_device: int) -> int:
    if current_index > len(input):
      return 0
    if current_index == len(input):
      jolt_diff = jolt_own_device - last_jolt
      return 1 if is_within_range(jolt_diff) else 0

    if current_index >= 0:
      jolt_diff = input[current_index] - last_jolt
      if not is_within_range(jolt_diff):
        return 0

      if current_index in memo.keys():
        return memo[current_index]

    current_jolt = input[current_index] if current_index >= 0 else 0
    next_index = current_index
    out = 0
    while next_index < len(input):
      next_index += 1
      out += compute_all_possible_adapter_combs(input, current_jolt, next_index, jolt_own_device)

    memo[current_index] = out

    return out
  
  return compute_all_possible_adapter_combs(input, -1, -1, jolt_own_device)


if __name__ == "__main__":
  input = read_input("/Users/danielgrittner/development/advent-of-code2020/day10/input.txt")
  # print(solve(input))
  print(solve2(input))
