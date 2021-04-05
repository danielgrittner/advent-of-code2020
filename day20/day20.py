"""
Day 20
"""
import copy
from functools import reduce
from math import sqrt
from typing import Tuple


def read_input(path: str):
  # Create a  tile id to tile hash map
  tiles = {}
  with open(path, 'r') as file_handle:
    line = file_handle.readline()
    while line != '':
      line = line[:-1] if line[-1] == '\n' else line
      # Line contains the tile id
      tile_id = int(line.split(' ')[-1][:-1])
      
      tile = []
      # A tile always is a 10 x 10 square
      for _ in range(10):
        line = file_handle.readline()
        line = line[:-1] if line[-1] == '\n' else line
        tile.append(line)

      tiles[tile_id] = tile

      line = file_handle.readline()  # Empty line
      line = file_handle.readline()  # Next tile

  return tiles


NUM_ROTATIONS = 8


def create_tile_id_to_rotations(tiles: dict) -> dict:
  tile_id_to_rotations = {}
  for tile_id in tiles.keys():
    tile_id_to_rotations[tile_id] = []

    """
    Rotation 1
         SIDE 1
      S          S
      I          I
      D          D
      E          E
      4          2
         SIDE 3
    """
    tile1_side1 = tiles[tile_id][0]
    tile1_side2 = ''.join([tiles[tile_id][i][-1] for i in range(10)])
    tile1_side3 = tiles[tile_id][-1]
    tile1_side4 = ''.join([tiles[tile_id][i][0] for i in range(10)])

    tile_id_to_rotations[tile_id].append([tile1_side1, tile1_side2, tile1_side3, tile1_side4])

    """
    Rotation 2
         4 EDIS
      S          S
      I          I
      D          D
      E          E
      3          1
         2 EDIS
    """
    tile2_side1 = tile1_side4[::-1]
    tile2_side2 = tile1_side1
    tile2_side3 = tile1_side2[::-1]
    tile2_side4 = tile1_side3

    tile_id_to_rotations[tile_id].append([tile2_side1, tile2_side2, tile2_side3, tile2_side4])

    """
    Rotation 3
         3 EDIS
      2          4
      E          E
      D          D
      I          I
      S          S
         1 EDIS
    """
    tile3_side1 = tile1_side3[::-1]
    tile3_side2 = tile1_side4[::-1]
    tile3_side3 = tile1_side1[::-1]
    tile3_side4 = tile1_side2[::-1]

    tile_id_to_rotations[tile_id].append([tile3_side1, tile3_side2, tile3_side3, tile3_side4])

    """
    Rotation 4
         SIDE 2 
      1          3
      E          E
      D          D
      I          I
      S          S
         SIDE 4
    """
    tile4_side1 = tile1_side2
    tile4_side2 = tile1_side3[::-1]
    tile4_side3 = tile1_side4
    tile4_side4 = tile1_side1[::-1]

    tile_id_to_rotations[tile_id].append([tile4_side1, tile4_side2, tile4_side3, tile4_side4])

    """
    Rotation 1 flipped
        1 EDIS
      S         S
      I         I
      D         D
      E         E
      2         4
        3 EDIS
    """
    tile5_side1 = tile1_side1[::-1]
    tile5_side2 = tile1_side4
    tile5_side3 = tile1_side3[::-1]
    tile5_side4 = tile1_side2

    tile_id_to_rotations[tile_id].append([tile5_side1, tile5_side2, tile5_side3, tile5_side4])

    """
    Rotation 2 flipped
         SIDE 4
      S          S
      I          I
      D          D
      E          E
      1          3
         SIDE 2
    """
    tile6_side1 = tile1_side4
    tile6_side2 = tile1_side3
    tile6_side3 = tile1_side2
    tile6_side4 = tile1_side1

    tile_id_to_rotations[tile_id].append([tile6_side1, tile6_side2, tile6_side3, tile6_side4])

    """
    Rotation 3 flipped
         SIDE 3
      4          2
      E          E
      D          D
      I          I
      S          S
         SIDE 1
    """
    tile7_side1 = tile1_side3
    tile7_side2 = tile1_side2[::-1]
    tile7_side3 = tile1_side1
    tile7_side4 = tile1_side4[::-1]

    tile_id_to_rotations[tile_id].append([tile7_side1, tile7_side2, tile7_side3, tile7_side4])

    """
    Rotation 4 flipped
         2 EDIS
      3          1
      E          E
      D          D
      I          I
      S          S
         4 EDIS
    """
    tile8_side1 = tile1_side2[::-1]
    tile8_side2 = tile1_side1[::-1]
    tile8_side3 = tile1_side4[::-1]
    tile8_side4 = tile1_side3[::-1]

    tile_id_to_rotations[tile_id].append([tile8_side1, tile8_side2, tile8_side3, tile8_side4])

  return tile_id_to_rotations


def get_matches_rotations_and_corners(tiles: dict) -> Tuple[dict, dict, list]:
  tile_id_to_rotations = create_tile_id_to_rotations(tiles)
  # Perform matching
  matches = {}
  for tile_id in tiles.keys():
    if tile_id not in matches.keys():
      matches[tile_id] = set()
    for tile_id2 in tiles.keys():
      if tile_id == tile_id2:
        continue

      # Check if tile_id and tile_id2 match
      match = False
      for rotation_tile1 in range(NUM_ROTATIONS):
        sides_tile1 = tile_id_to_rotations[tile_id][rotation_tile1]
        for rotation_tile2 in range(NUM_ROTATIONS):
          sides_tile2 = tile_id_to_rotations[tile_id2][rotation_tile2]

          for side1 in range(4):
            for side2 in range(4):
              if sides_tile1[side1] == sides_tile2[side2]:
                match = True
                break
            if match:
              break

          if match:
            break
        if match:
          break

      if match:
        matches[tile_id].add(tile_id2)
        if tile_id2 not in matches.keys():
          matches[tile_id2] = set()
        matches[tile_id2].add(tile_id)

  corner_tile_ids = []
  for tile_id in matches.keys():
    if len(matches[tile_id]) == 2:
      corner_tile_ids.append(tile_id)

  return matches, tile_id_to_rotations, corner_tile_ids


def solve1(tiles: dict) -> int:
  _, _, corners = get_matches_rotations_and_corners(tiles)
  assert len(corners) == 4
  return reduce(lambda x, y: x * y, corners)


"""
  Sea monster:
 |                  #   |  pos (0 indexed) of # in row 1: 18
 |#    ##    ##    ###  |  pos (0 indexed) of # in row 2: 0, 5, 6, 11, 12, 17, 18, 19
 | #  #  #  #  #  #     |  pos (0 indexed) of # in row 3: 1, 4, 7, 10, 13, 16
"""
MONSTER_ROW1 = [18]
MONSTER_ROW2 = [0, 5, 6, 11, 12, 17, 18, 19]
MONSTER_ROW3 = [1, 4, 7, 10, 13, 16]


TOP_INDEX = 0
RIGHT_INDEX = 1
BOTTOM_INDEX = 2
LEFT_INDEX = 3


def compute_tile_grid(num_tiles: int, matches: dict, tile_id_to_rotations: dict, corners: list) -> list:
  img_side_length = int(sqrt(num_tiles))
  # We store tuples in the grid. The first element is the tile id and the second the rotation
  grid =[[(-1, -1) for _ in range(img_side_length)] for _ in range(img_side_length)]
  # We just start with some random tile in the upper left corner
  grid[0][0] = (corners[0], -1)

  # We need to find the correct rotation for the tile in the left corner and 
  # then we can just keep adding the other tiles in the fitting rotation.

  # Find the correct rotation for the left corner
  tile_id_left_corner = corners[0]
  match = list(matches[tile_id_left_corner])
  for rot in range(NUM_ROTATIONS):
    right_side = tile_id_to_rotations[tile_id_left_corner][rot][RIGHT_INDEX]
    bottom_side = tile_id_to_rotations[tile_id_left_corner][rot][BOTTOM_INDEX]

    # Check if right side matches with something and then the bottom matches the other tile
    right_side_candidate = match[0]
    bottom_side_candidate = match[1]

    right = [tile_id_to_rotations[right_side_candidate][rot][LEFT_INDEX] == right_side for rot in range(NUM_ROTATIONS)]
    bottom = [tile_id_to_rotations[bottom_side_candidate][rot][TOP_INDEX] == bottom_side for rot in range(NUM_ROTATIONS)]
    if any(right) and any(bottom):
        grid[0][0] = (tile_id_left_corner, rot)
        break

    # Try the other way around
    right_side_candidate = match[1]
    bottom_side_candidate = match[0]

    right = [tile_id_to_rotations[right_side_candidate][rot][LEFT_INDEX] == right_side for rot in range(NUM_ROTATIONS)]
    bottom = [tile_id_to_rotations[bottom_side_candidate][rot][TOP_INDEX] == bottom_side for rot in range(NUM_ROTATIONS)]
    if any(right) and any(bottom):
        grid[0][0] = (tile_id_left_corner, rot)
        break

  # Now, we can expand the grid and always add for a position the matching bottom and right part 
  for i in range(img_side_length - 1):
    for j in range(img_side_length):
      tile_id, rotation = grid[i][j]
      match = list(matches[tile_id])

      right_side = tile_id_to_rotations[tile_id][rotation][RIGHT_INDEX]
      bottom_side = tile_id_to_rotations[tile_id][rotation][BOTTOM_INDEX]

      # We first find the bottom tile and its rotation
      for candidate_tile_id in match:
        candidate = [tile_id_to_rotations[candidate_tile_id][rot][TOP_INDEX] == bottom_side for rot in range(NUM_ROTATIONS)]
        if any(candidate):
          # It's a match!
          candidate_rotation = list(filter(lambda t: t[1], enumerate(candidate)))[0][0]
          grid[i + 1][j] = (candidate_tile_id, candidate_rotation)
          break

      # If the current tile is located at the right border, we skip searching for the right side
      # since there is none.
      if j + 1 < img_side_length:
        for candidate_tile_id in match:
          candidate = [tile_id_to_rotations[candidate_tile_id][rot][LEFT_INDEX] == right_side for rot in range(NUM_ROTATIONS)]
          if any(candidate):
            # It's a match!
            candidate_rotation = list(filter(lambda t: t[1], enumerate(candidate)))[0][0]
            grid[i][j + 1] = (candidate_tile_id, candidate_rotation)
            break

  return grid


def rotate_square_90_deg_right(square: list) -> list:
  square_copy = copy.deepcopy(square)
  square_copy = list(map(lambda row: list(row), square_copy))
  for i in range(len(square)):
    for j in range(len(square)):
      square_copy[j][len(square) - i - 1] = square[i][j]
  square_copy = list(map(lambda row: ''.join(row), square_copy))
  return square_copy


def rotate_square_180_deg_right(square: list) -> list:
  square_copy = copy.deepcopy(square)
  square_copy = list(map(lambda row: list(row), square_copy))
  for i in range(len(square)):
    for j in range(len(square)):
      square_copy[len(square) - i - 1][len(square) - j - 1] = square[i][j]
  square_copy = list(map(lambda row: ''.join(row), square_copy))
  return square_copy


def rotate_square_270_deg_right(square: list) -> list:
  square_copy = copy.deepcopy(square)
  square_copy = list(map(lambda row: list(row), square_copy))
  for i in range(len(square)):
    for j in range(len(square)):
      square_copy[len(square)- j - 1][i] = square[i][j]
  square_copy = list(map(lambda row: ''.join(row), square_copy))
  return square_copy


def flip_square(square: list) -> list:
  for row in range(len(square)):
    square[row] = square[row][::-1]
  return square


def rotate_and_flip_square(square: list, rotation: int) -> list:
  if rotation == 0:
    """
    Rotation 1 = no rotation
         SIDE 1
      S          S
      I          I
      D          D
      E          E
      4          2
         SIDE 3
    """
    return square
  elif rotation == 1:
    """
    Rotation 2
         4 EDIS
      S          S
      I          I
      D          D
      E          E
      3          1
         2 EDIS
    """
    return rotate_square_90_deg_right(square)
  elif rotation == 2:
    """
    Rotation 3
         3 EDIS
      2          4
      E          E
      D          D
      I          I
      S          S
         1 EDIS
    """
    return rotate_square_180_deg_right(square)
  elif rotation == 3:
    """
    Rotation 4
         SIDE 2 
      1          3
      E          E
      D          D
      I          I
      S          S
         SIDE 4
    """
    return rotate_square_270_deg_right(square)
  elif rotation == 4:
    """
    Rotation 1 flipped
        1 EDIS
      S         S
      I         I
      D         D
      E         E
      2         4
        3 EDIS
    """
    return flip_square(square)
  elif rotation == 5:
    """
    Rotation 2 flipped
         SIDE 4
      S          S
      I          I
      D          D
      E          E
      1          3
         SIDE 2
    """
    return flip_square(rotate_square_90_deg_right(square))
  elif rotation == 6:
    """
    Rotation 3 flipped
         SIDE 3
      4          2
      E          E
      D          D
      I          I
      S          S
         SIDE 1
    """
    return flip_square(rotate_square_180_deg_right(square))
  else:
    """
    Rotation 4 flipped
         2 EDIS
      3          1
      E          E
      D          D
      I          I
      S          S
         4 EDIS
    """
    assert rotation == 7
    return flip_square(rotate_square_270_deg_right(square))


def get_tile_in_correct_rotation(tiles: dict, tile_id: int, rotation: int) -> list:
  tile = tiles[tile_id]
  assert len(tile) == len(tile[0])
  return rotate_and_flip_square(tile, rotation)


def get_image(grid: list, tiles: dict) -> list:
  image = []

  for row in range(len(grid)):
    block = []
    for col in range(len(grid)):
      tile_id, rot = grid[row][col]
      tile = get_tile_in_correct_rotation(tiles, tile_id, rot)

      # The border of a tile is not part of the image
      tile = tile[1:]
      tile = [tile_row[:-1] for tile_row in tile]
      tile = tile[:-1]
      tile = [tile_row[1:] for tile_row in tile]
      
      for i, row_tile in enumerate(tile):
        if i >= len(block):
          block.append('')
        block[i] += row_tile

    image += block

  return image


def is_monster(image: list, start_row: int, start_col: int) -> bool:
  for offset in MONSTER_ROW1:
    if image[start_row][start_col + offset] != '#':
      return False

  start_row += 1
  for offset in MONSTER_ROW2:
    if image[start_row][start_col + offset] != '#':
      return False

  start_row += 1
  for offset in MONSTER_ROW3:
    if image[start_row][start_col + offset] != '#':
      return False

  return True


def contains_sea_monster(image: list) -> bool:
  for row in range(len(image) - 2):
    for col in range(len(image) - 19):
      if is_monster(image, row, col):
        return True
  return False


def count_hashes_not_part_of_sea_monsters(image: list) -> int:
  bitset = [[x == '#' for x in image[row]] for row in range(len(image))]

  for row in range(len(image) - 2):
    for col in range(len(image) - 19):
      if is_monster(image, row, col):
        for offset in MONSTER_ROW1:
          bitset[row][col + offset] = False

        for offset in MONSTER_ROW2:
          bitset[row + 1][col + offset] = False

        for offset in MONSTER_ROW3:
          bitset[row + 2][col + offset] = False

  # Now, count the number of True values in bitset
  num_remaining_hashes = sum(map(lambda row: sum(filter(lambda x: x, row)), bitset))
  return num_remaining_hashes


def print_image(image: list) -> None:
  for row in image:
    print(row)
  print(f'{len(image), len(image[0])}')

def solve2(tiles: dict) -> int:
  num_tiles = len(tiles.keys())
  matches, tile_id_to_rotations, corners = get_matches_rotations_and_corners(tiles)

  # We now need to build up the grid how we structure the image (the exact orientation does not matter)
  grid = compute_tile_grid(num_tiles, matches, tile_id_to_rotations, corners)
  image = get_image(grid, tiles)
  orig_image = copy.deepcopy(image)

  # Rotate the image until there is at least 1 sea monster
  for rot in range(NUM_ROTATIONS):
    image = rotate_and_flip_square(orig_image, rot)
    if contains_sea_monster(image):
      break
  # assert contains_sea_monster(image)  # Sanity check

  # Count all # which are not part of a sea monster
  roughness = count_hashes_not_part_of_sea_monsters(image)
  return roughness


if __name__ == "__main__":
  file_name = 'input.txt'
  input = read_input(f'/Users/danielgrittner/development/advent-of-code2020/day20/{file_name}')
  # # print(solve1(input))
  print(solve2(input))
