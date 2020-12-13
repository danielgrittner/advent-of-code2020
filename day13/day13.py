"""
Day 13
"""
from typing import Tuple
import math


def read_input(path: str) -> Tuple[int, list]:
  with open(path, "r") as file_handle:
    departure_time = int(file_handle.readline()[:-1])
    bus_ids = file_handle.readline().split(",")

  return departure_time, bus_ids


def solve(departure_time: int, bus_ids: list) -> int:
  # Compute the last departures
  min_departure = math.inf
  min_departure_bus_id = None

  for bus_id in bus_ids:
    if bus_id != 'x':
      bus_id = int(bus_id)
      number_of_past_rides = departure_time // bus_id
      last_departure = number_of_past_rides * bus_id
      # Add a new departure
      last_departure += bus_id

      if last_departure >= departure_time and last_departure < min_departure:
        min_departure = last_departure
        min_departure_bus_id = bus_id

  return (min_departure - departure_time) * min_departure_bus_id


def solve2(bus_ids: list) -> int:
  bus_ids_int = list(map(lambda x: int(x), filter(lambda x: x != 'x', bus_ids)))
  bus_offsets = list(map(lambda x: x[1], filter(lambda x: x[0] != 'x', zip(bus_ids, range(len(bus_ids))))))
  
  current_multiple = bus_ids_int[0]
  extender = bus_ids_int[0]

  for i in range(1, len(bus_ids_int)):
    while True:
      if (current_multiple + bus_offsets[i]) % bus_ids_int[i] == 0:
        extender *= bus_ids_int[i]
        break
      current_multiple += extender

  return current_multiple


if __name__ == "__main__":
  departure_time, bus_ids = read_input("/Users/danielgrittner/development/advent-of-code2020/day13/input.txt")
  # print(solve(departure_time, bus_ids))
  print(solve2(bus_ids))
  