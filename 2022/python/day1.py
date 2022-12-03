# https://adventofcode.com/2022/day/1

import os
from pathlib import Path
from typing import List, Union


def load_data(path: Union[str, bytes, os.PathLike]) -> List[List[int]]:
    with open(path) as fd:
        return [[int(item) for item in items.splitlines()] for items in fd.read().split("\n\n")]


def part_one(data: List[List[int]]) -> int:
    return max(sum(food) for food in data)


def part_two(data: List[List[int]]) -> int:
    return sum(sum(elf) for elf in sorted(data, key=sum)[-3:])


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/01"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 24000
    assert part_two(samples) == 45000

    print(part_one(data))
    print(part_two(data))
