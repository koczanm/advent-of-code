# https://adventofcode.com/2021/day/7

from math import ceil, floor
from operator import add
from pathlib import Path
from statistics import mean, median


def load_data(path):
    with open(path) as fd:
        return [int(pos) for pos in fd.read().split(",")]


def part_one(data):
    target = floor(median(data))
    return sum([abs(target - pos) for pos in data])


def part_two(data):
    mean_pos = mean(data)
    targets = [floor(mean_pos), ceil(mean_pos)]
    results = [0] * len(targets)
    for pos in data:
        diffs = [abs(target - pos) for target in targets]
        sums = [diff * (diff + 1) // 2 for diff in diffs]
        results = list(map(add, results, sums)) 
    return min(results)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/07/"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 37
    assert part_two(samples) == 168

    print(part_one(data))
    print(part_two(data))

