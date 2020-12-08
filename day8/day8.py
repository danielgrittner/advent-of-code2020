"""
Day 8
"""
from typing import Tuple


def read_input(path: str) -> list:
  instructions = []
  with open(path, "r") as file_handle:
    line = file_handle.readline()
    while line != '':
      line = line[:-1] if line[-1] == '\n' else line  # Remove line break
      splitted = line.split()
      operation = splitted[0]
      value = int(splitted[1][1:])
      if splitted[1][0] == '-':
        value *= -1
      instructions.append({"op": operation, "val": value})
      line = file_handle.readline()

  return instructions


def solve(input: list) -> int:
  accumulator = 0

  instruction_pointer = 0
  visited = set()

  while instruction_pointer < len(input) and instruction_pointer >= 0:
    if instruction_pointer in visited:
      break
    visited.add(instruction_pointer)

    next_instruction = input[instruction_pointer]["op"]
    value = input[instruction_pointer]["val"]

    if next_instruction == "nop":
      instruction_pointer += 1
    elif next_instruction  == "acc":
      accumulator += value
      instruction_pointer += 1
    else: # jmp
      instruction_pointer += value

  return accumulator


def solve2(input: list) -> int:
  """
    TODO: ugly as hell (answer: 1000, in case I want to improve the code later on)
  """
  visited = set()
  changed = set()

  def search(instruction_pointer: int, accumulator: int) -> Tuple[bool, int]:
    if instruction_pointer >= len(input):
      return True, accumulator

    if instruction_pointer in visited:
      return False, None

    visited.add(instruction_pointer)

    if input[instruction_pointer]["op"] == "acc":
      success, acc = search(instruction_pointer + 1, accumulator + input[instruction_pointer]["val"])
      if not success:
        return success, None
      return success, acc

    if input[instruction_pointer]["op"] == "nop":
      success, acc = search(instruction_pointer + 1, accumulator)
      if not success:
        if len(changed) > 0:
          return False, None
        changed.add(instruction_pointer)

        # Turn nop into a jmp
        success, acc = search(instruction_pointer + input[instruction_pointer]["val"], accumulator)
        if not success:
          changed.pop()
          return success, None
        return success, acc

      return success, acc

    # "jmp"
    success, acc = search(instruction_pointer + input[instruction_pointer]["val"], accumulator)
    if not success:
      if len(changed) > 0:
        return False, None
      changed.add(instruction_pointer)
      success, acc = search(instruction_pointer + 1, accumulator)
      if not success:
        changed.pop()
        return success, None
      return success, acc
    return success, acc

  _, final_acc = search(0, 0)
  return final_acc


if __name__ == "__main__":
  instructions = read_input("/Users/danielgrittner/development/advent-of-code2020/day8/input.txt")
  print(solve(instructions))

  print(solve2(instructions))
