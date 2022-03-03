# https://adventofcode.com/2021/day/17

import re
from collections import namedtuple, deque
from itertools import product
from pathlib import Path


Position = namedtuple("Position", "x y")
Target = namedtuple("Target", "xmin xmax ymin ymax")


def load_data(path):
    with open(path) as fd:
        coords = [int(coord) for coord in re.findall(r"-?\d+", fd.read())]
        return Target(*coords)


def launch_probe(vx, vy):
    position = Position(0, 0)
    while True:
        yield position
        position = Position(position.x + vx, position.y + vy)
        vx, vy = max(0, vx - 1), vy - 1


def is_hit(vx, vy, target):
    for position in launch_probe(vx, vy):
        if target.xmin <= position.x <= target.xmax and target.ymin <= position.y <= target.ymax:
            return True
        elif position.x > target.xmax or position.y < target.ymin:
            return False


def get_acc_vy_range(vx, vy_init, target):
    vy_range = deque()
    for vy in range(vy_init, -target.ymin + 1):
        if is_hit(vx, vy, target):
            vy_range.appendleft(vy)
    return vy_range


def get_acc_velocities(target):
    acc_velocities = []
    for vx in range(0, target.xmax + 1):
        for vy in range(target.ymin, -target.ymin):
            if is_hit(vx, vy, target):
                acc_velocities.append((vx, vy))
    return acc_velocities


def part_one(data):
    return data.ymin * (data.ymin + 1) // 2


def part_two(data):
    velocities = get_acc_velocities(data)
    return len(velocities)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/17"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 45
    assert part_two(samples) == 112

    print(part_one(data))
    print(part_two(data))
