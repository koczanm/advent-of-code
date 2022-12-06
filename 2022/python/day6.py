# https://adventofcode.com/2022/day/6

import os
from collections import Counter
from pathlib import Path
from typing import Union


def load_data(path: Union[str, bytes, os.PathLike]) -> str:
    with open(path) as fd:
        return fd.read().strip()


def find_marker(data: str, unique_chars_num: int = 4) -> int:
    counter = Counter(data[:unique_chars_num])
    tail_idx = 0
    for head in data[unique_chars_num:]:
        if len(counter.keys()) == unique_chars_num:
            break
        tail = data[tail_idx]
        counter[tail] -= 1
        counter[head] += 1
        if counter[tail] == 0:
            del counter[tail]
        tail_idx += 1
    return tail_idx + unique_chars_num


def part_one(data: str) -> int:
    return find_marker(data)


def part_two(data: str) -> int:
    return find_marker(data, unique_chars_num=14)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/06"
    samples1 = load_data(input_dir / "samples1.in")
    samples2 = load_data(input_dir / "samples2.in")
    samples3 = load_data(input_dir / "samples3.in")
    samples4 = load_data(input_dir / "samples4.in")
    samples5 = load_data(input_dir / "samples5.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples1) == 7
    assert part_one(samples2) == 5
    assert part_one(samples3) == 6
    assert part_one(samples4) == 10
    assert part_one(samples5) == 11
    assert part_two(samples1) == 19
    assert part_two(samples2) == 23
    assert part_two(samples3) == 23
    assert part_two(samples4) == 29
    assert part_two(samples5) == 26

    print(part_one(data))
    print(part_two(data))
