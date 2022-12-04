# https://adventofcode.com/2022/day/3

import os
from pathlib import Path
from typing import List, Union

LOWERCASE_OFFSET = ord("a") - 1
UPPERCASE_OFFSET = ord("A") - 27


def load_data(path: Union[str, bytes, os.PathLike]) -> List[str]:
    with open(path) as fd:
        return fd.read().splitlines()


def find_common(*data: str) -> str:
    first_line, *rest = data
    return set(first_line).intersection(*rest).pop()


def get_priority(item: str) -> int:
    if item.islower():
        return ord(item) - LOWERCASE_OFFSET
    else:
        return ord(item) - UPPERCASE_OFFSET


def part_one(data: List[str]) -> int:
    priority_sum = 0
    for rucksack in data:
        common = find_common(rucksack[: len(rucksack) // 2], rucksack[len(rucksack) // 2 :])
        priority_sum += get_priority(common)
    return priority_sum


def part_two(data: List[str]) -> int:
    priority_sum = 0
    for group in zip(*[iter(data)] * 3):
        common = find_common(*group)
        priority_sum += get_priority(common)
    return priority_sum


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/03"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 157
    assert part_two(samples) == 70

    print(part_one(data))
    print(part_two(data))
