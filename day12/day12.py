"""
Day 12
"""


def read_input(path: str) -> list:
	out = []
	with open(path, "r") as file_handle:
		line = file_handle.readline()
		while line != '':
			line = line[:-1] if line[-1] == '\n' else line
			out.append((line[0], int(line[1:])))
			line = file_handle.readline()
	return out


class Direction:
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3


def solve(actions: list) -> int:
	# Direction: 0 == north, 1 == east, 2 == south, 3 == west
	direction = Direction.EAST
	x = 0
	y = 0

	for action, val in actions:
		if action == 'N':
			y += val
		elif action == 'E':
			x += val
		elif action == 'S':
			y -= val
		elif action == 'W':
			x -= val
		elif action == 'L':
			direction = (direction - (val // 90)) % 4
		elif action == 'R':
			direction = (direction + (val // 90)) % 4
		elif action == 'F':
			if direction == Direction.NORTH:
				y += val
			elif direction == Direction.EAST:
				x += val
			elif direction == Direction.SOUTH:
				y -= val
			elif direction == Direction.WEST:
				x -= val
			else:
				raise ValueError(f'Invalid direction.')
		else:
			raise ValueError(f'Invalid action: {action}')

	return abs(x) + abs(y)


def solve2(actions: list) -> int:
	x = 0
	y = 0

	waypoint_x = 10
	waypoint_y = 1

	for action, val in actions:
		if action == 'N':
			waypoint_y += val
		elif action == 'E':
			waypoint_x += val
		elif action == 'S':
			waypoint_y -= val
		elif action == 'W':
			waypoint_x -= val
		elif action == 'L':
			rotate_left = (val // 90) % 4
			while rotate_left > 0:
				temp_x = -1
				temp_y = -1

				temp_y = waypoint_x
				temp_x = -waypoint_y

				waypoint_x = temp_x 
				waypoint_y = temp_y

				rotate_left -= 1
		elif action == 'R':
			rotate_right = (val // 90) % 4
			while rotate_right > 0:
				temp_x = -1
				temp_y = -1

				temp_y = -waypoint_x
				temp_x = waypoint_y

				waypoint_x = temp_x
				waypoint_y = temp_y
				
				rotate_right -= 1
		elif action == 'F':
			x += val * waypoint_x
			y += val * waypoint_y
		else:
			raise ValueError(f'Invalid action: {action}')

	return abs(x) + abs(y)


if __name__ == "__main__":
	actions = read_input("/Users/danielgrittner/development/advent-of-code2020/day12/input.txt")
	# print(solve(actions))
	print(solve2(actions))
	
			