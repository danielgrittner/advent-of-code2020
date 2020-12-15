"""
Day 14
"""
from gmpy2 import xmpz


class Instruction:
  MASK = 0
  MEM = 1


def apply_bitmask_to_num(mask: str, num: int) -> int:
  num = xmpz(num)
  for i in range(36):
    if mask[i] == '1':
      num[i] = 1
    elif mask[i] == '0':
      num[i] = 0
  return int(num)


def apply_power_bitmask_to_num(mask: str, num: int) -> list:
  queue = [xmpz(num)]

  for i in range(36):
    if mask[i] == '1':
      for j in range(len(queue)):
        queue[j][i] = 1
    elif mask[i] == 'X':
      new_queue = []
      for ele in queue:
        ele1 = ele.copy()
        ele1[i] = 0
        new_queue.append(ele1)
        
        ele2 = ele.copy()
        ele2[i] = 1
        new_queue.append(ele2)

      queue = new_queue

  return [int(x) for x in queue]


def parse_instruction(line: str) -> dict:
  """
  Instructions are of the following form:
  - "mask = val"
  - "mem[adr] = val"
  """
  line_split = line.split()
  if line_split[0] == "mask":
    return {
      "instr": Instruction.MASK,
      "val": line_split[-1][::-1]
    }
  else: # is mem
    return {
      "instr": Instruction.MEM,
      "adr": int(line_split[0][len("mem["):][:-1]),
      "val": int(line_split[-1])
    }


def read_input(path: str) -> list:
  program = []
  with open(path, "r") as file_handle:
    line = file_handle.readline()
    while line != '':
      line = line[:-1] if line[-1] == '\n' else line
      program.append(parse_instruction(line))
      line = file_handle.readline()
  return program


def solve(program: list) -> int:
  memory = {}
  mask = program[0]["val"]  # First value is always the initial mask

  for instr in program[1:]:
    if instr["instr"] == Instruction.MASK:
      mask = instr["val"]
    elif instr["instr"] == Instruction.MEM:
      memory[instr["adr"]] = apply_bitmask_to_num(mask, instr["val"])
    else:
      raise ValueError(f'Invalid instruction type: {instr["instr"]}')

  out = 0
  for adr in memory.keys():
    out += memory[adr]

  return out


def solve2(program: list) -> int:
  memory = {}
  mask = program[0]["val"]

  for instr in program[1:]:
    if instr["instr"] == Instruction.MASK:
      mask = instr["val"]
    elif instr["instr"] == Instruction.MEM:
      memory_addresses = apply_power_bitmask_to_num(mask, instr["adr"])
      for memory_address in memory_addresses:
        memory[memory_address] = instr["val"]
    else:
      raise ValueError(f'Invalid instruction type: {instr["instr"]}')

  out = 0
  for adr in memory.keys():
    out += memory[adr]

  return out


if __name__ == "__main__":
  program = read_input("/Users/danielgrittner/development/advent-of-code2020/day14/input.txt")
  # print(solve(program))
  print(solve2(program))
