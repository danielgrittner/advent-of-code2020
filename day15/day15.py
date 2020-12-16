"""
Day 15
"""

def solve(input: list, threshold: int = 2020) -> int:
  nums = {}
  for i, num in enumerate(input):
    nums[num] = i + 1
  
  ith_num = len(input) + 1
  last_num = 0

  while ith_num < threshold:
    if last_num not in nums.keys():
      nums[last_num] = ith_num
      last_num = 0
      ith_num += 1
    else:
      diff = ith_num - nums[last_num]
      nums[last_num] = ith_num
      last_num = diff
      ith_num += 1

  return last_num


if __name__ == "__main__":
  input = [9, 3, 1, 0, 8, 4]
  # test = [0,3,6]
  # Solve 1
  print(solve(input))
  # Solve 2 - brute force :D
  print(solve(input, threshold=30000000))

