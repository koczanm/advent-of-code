# https://adventofcode.com/2022/day/4

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple, Union


class Range:
    start: int
    end: int

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def __contains__(self, item: Union[int, Range]) -> bool:
        if isinstance(item, int):
            return self.start <= item <= self.end
        return self.start <= item.start and self.end >= item.end


def load_data(path: Union[str, bytes, os.PathLike]) -> List[Tuple[Range, Range]]:
    assingments = []
    with open(path) as fd:
        for line in fd:
            assingment = [Range(*[int(id_num) for id_num in range_.split("-")]) for range_ in line.strip().split(",")]
            assingments.append(assingment)
    return assingments


def part_one(data: List[Tuple[Range, Range]]) -> int:
    result = 0
    for first_range, second_range in data:
        result += bool(first_range in second_range or second_range in first_range)
    return result


def part_two(data: List[Tuple[Range, Range]]) -> int:
    result = 0
    for first_range, second_range in data:
        result += bool(
            first_range.start in second_range
            or first_range.end in second_range
            or second_range.start in first_range
            or second_range.end in first_range
        )
    return result


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/04"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 2
    assert part_two(samples) == 4

    print(part_one(data))
    print(part_two(data))
