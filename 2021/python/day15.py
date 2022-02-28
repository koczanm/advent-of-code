# https://adventofcode.com/2021/day/15

from collections import namedtuple
from copy import deepcopy
from pathlib import Path
from queue import PriorityQueue


Position = namedtuple("Position", "x y")


def load_data(path):
    values = []
    with open(path) as fd:
        for line in fd:
            values.append([int(x) for x in line.strip()])
    return values


def get_neighbors(position, max_x, max_y):
    x, y = position
    neighbors = []
    if x > 0:
        neighbors.append(Position(x - 1, y))
    if x < max_x:
        neighbors.append(Position(x + 1, y))
    if y > 0:
        neighbors.append(Position(x, y - 1))
    if y < max_y:
        neighbors.append(Position(x, y + 1))
    return neighbors


def get_manhattan_distance(position_a, position_b):
    return abs(position_a.x - position_b.x) + abs(position_a.y - position_b.y)


def find_lowest_risk(risk_map):
    max_x = len(risk_map[0]) - 1
    max_y = len(risk_map) - 1
    start = Position(0, 0)
    end = Position(max_x, max_y)
    total_risk_map = [[float("inf")] * (max_y + 1) for _ in range(max_x + 1)]
    total_risk_map[start.y][start.x] = 0
    queue = PriorityQueue()
    queue.put((-1, start))  # priority is irrelevant for the starting point
    while not queue.empty():
        priority, position = queue.get()
        if position == end:
            return total_risk_map[position.y][position.x]
        for neighbor in get_neighbors(position, max_x, max_y):
            new_risk = total_risk_map[position.y][position.x] + risk_map[neighbor.y][neighbor.x]
            if new_risk < total_risk_map[neighbor.y][neighbor.x]:
                total_risk_map[neighbor.y][neighbor.x] = new_risk
                priority = new_risk + get_manhattan_distance(neighbor, end)
                queue.put((priority, neighbor))


def get_full_map(risk_map, multiplier=4):
    full_risk_map = deepcopy(risk_map)
    original_width = len(risk_map[0])
    original_height = len(risk_map)
    for i in range(multiplier):
        for row in full_risk_map:
            row.extend([risk % 9 + 1 for risk in row[-original_width:]])
        for row in full_risk_map[original_height * i : original_height * (i + 1)]:
            new_row = [risk % 9 + 1 for risk in row]
            full_risk_map.append(new_row)
    return full_risk_map


def part_one(data):
    return find_lowest_risk(data)


def part_two(data):
    full_data = get_full_map(data)
    return find_lowest_risk(full_data)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/15"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 40
    assert part_two(samples) == 315

    print(part_one(data))
    print(part_two(data))
