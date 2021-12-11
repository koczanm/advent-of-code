# https://adventofcode.com/2021/day/6

from collections import deque
from pathlib import Path


MAX_FISH_AGE = 8


def load_data(path):
    with open(path) as fd:
        return [int(fish) for fish in fd.read().split(",")]


def simulate(fish, days_num=80):
    fish_counter = deque([fish.count(i) for i in range(MAX_FISH_AGE + 1)])
    for _ in range(days_num):
        fish_counter[7] += fish_counter[0]
        fish_counter.rotate(-1)

    return sum(fish_counter)


def part_one(data):
    return simulate(data)


def part_two(data):
    return simulate(data, 256)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/06/"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 5934
    assert part_two(samples) == 26984457539

    print(part_one(data))
    print(part_two(data))
