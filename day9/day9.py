"""
Day 9
"""
from typing import Optional, Tuple


def read_input(path: str) -> list:
  out = []
  with open(path, "r") as file_handle:
    line = file_handle.readline()
    while line != '':
      out.append(int(line[:-1]))
      line = file_handle.readline()
  return out


def has_add_match(target: int, nums: list) -> bool:
  for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
      if nums[i] + nums[j] == target:
        return True
  return False


def solve(nums: list, preamble: int = 25) -> Optional[int]:
  for i in range(preamble, len(nums)):
    current_num = nums[i]
    prevs = nums[i - preamble:i]
    if not has_add_match(current_num, prevs):
      return current_num
  return None


def min_max_within_range(nums: list, start: int, end: int) -> Tuple[int, int]:
  min_ele = nums[start]
  max_ele = nums[start]

  while start <= end:
    if nums[start] < min_ele:
      min_ele = nums[start]
    if nums[start] > max_ele:
      max_ele = nums[start]
    start += 1

  return min_ele, max_ele


def solve2(nums: list) -> Optional[int]:
  invalid_num = solve(nums)

  current_sum = nums[0]
  length_of_sequence = 1

  start = 0
  end = 0

  while end < len(nums):
    if current_sum == invalid_num and length_of_sequence >= 2:
      min_ele, max_ele = min_max_within_range(nums, start, end)
      return min_ele + max_ele

    if current_sum < invalid_num:
      end += 1
      current_sum += nums[end]
      length_of_sequence += 1
    elif current_sum > invalid_num and start < end:
      current_sum -= nums[start]
      length_of_sequence -= 1
      start += 1
    else:
      start += 1
      end = start
      current_sum = nums[end]
      length_of_sequence = 1

  return None
  

if __name__ == "__main__":
  data = read_input("/Users/danielgrittner/development/advent-of-code2020/day9/input.txt")
  # print(solve(data))
  print(solve2(data))
