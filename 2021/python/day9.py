# https://adventofcode.com/2021/day/9

import math
from collections import namedtuple
from pathlib import Path


Point = namedtuple("Point", "x y")
HeightMap = namedtuple("HeightMap", "values max_x max_y")


def load_data(path):
    values = []
    with open(path) as fd:
        for line in fd:
            values.append([int(value) for value in line.strip()])
    max_x = len(values[0]) - 1
    max_y = len(values) - 1
    return HeightMap(values, max_x, max_y)


def get_neighbors(x, y, max_x, max_y):
    neighbors = []
    if x > 0:
        neighbors.append(Point(x - 1, y))
    if x < max_x:
        neighbors.append(Point(x + 1, y))
    if y > 0:
        neighbors.append(Point(x, y - 1))
    if y < max_y:
        neighbors.append(Point(x, y + 1))
    return neighbors


def get_low_points(heightmap):
    low_points = []
    for y, row in enumerate(heightmap.values):
        for x, height in enumerate(row):
            neighbors = get_neighbors(x, y, heightmap.max_x, heightmap.max_y)
            if all(height < heightmap.values[neighbor.y][neighbor.x] for neighbor in neighbors):
                low_points.append((Point(x, y)))
    return low_points


def get_risk(heightmap):
    return sum(heightmap.values[point.y][point.x] + 1 for point in get_low_points(heightmap))


def flood_fill(heightmap, visited, x, y):
    if not visited[y][x]:
        visited[y][x] = True
        basin_size = 0
        for neighbor in get_neighbors(x, y, heightmap.max_x, heightmap.max_y):
            if heightmap.values[neighbor.y][neighbor.x] < 9:
                basin_size += flood_fill(heightmap, visited, neighbor.x, neighbor.y)
        return basin_size + 1
    return 0


def get_basins(heightmap, top=1):
    visited = [[False] * (heightmap.max_x + 1) for _ in range(heightmap.max_y + 1)]
    basins = []
    for y, row in enumerate(heightmap.values):
        for x, height in enumerate(row):
            if height < 9:
                basins.append(flood_fill(heightmap, visited, x, y))
    return sorted(basins, reverse=True)[:top]


def part_one(data):
    return get_risk(data)


def part_two(data):
    return math.prod(get_basins(data, top=3))


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/09"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 15
    assert part_two(samples) == 1134

    print(part_one(data))
    print(part_two(data))
