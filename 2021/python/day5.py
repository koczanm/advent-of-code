# https://adventofcode.com/2021/day/5

import re
from collections import defaultdict, namedtuple
from itertools import takewhile
from pathlib import Path


Point = namedtuple("Point", "x y")
Vent = namedtuple("Vent", "start end")


def load_data(path):
    with open(path) as fd:
        vents = []
        for line in fd:
            x1, y1, x2, y2 = (int(coord) for coord in re.findall(r"\d+", line))
            vents.append(Vent(Point(x1, y1), Point(x2, y2)))
    return vents


def count_overlaps(vents):
    marked_points = defaultdict(int)
    for vent in vents:
        slope_x = vent.end.x - vent.start.x
        slope_y = vent.end.y - vent.start.y
        dx = 0 if slope_x == 0 else slope_x // abs(slope_x)
        dy = 0 if slope_y == 0 else slope_y // abs(slope_y)
        curr_point = vent.start
        marked_points[curr_point] += 1
        while curr_point != vent.end:
            curr_point = Point(curr_point.x + dx, curr_point.y + dy)
            marked_points[curr_point] += 1
    return len([point for point, count in marked_points.items() if count > 1])


def part_one(data):
    data = [vent for vent in data if vent.start.x == vent.end.x or vent.start.y == vent.end.y]
    return count_overlaps(data)


def part_two(data):
    return count_overlaps(data)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/05/"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 5
    assert part_two(samples) == 12

    print(part_one(data))
    print(part_two(data))
