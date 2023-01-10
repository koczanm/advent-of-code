# https://adventofcode.com/2022/day/13

import os
from functools import cmp_to_key
from itertools import zip_longest
from pathlib import Path

Packet = int | list["Packet"]


def load_data(path: str | bytes | os.PathLike) -> list[Packet]:
    packets = []
    with open(path) as fd:
        for line in fd:
            if line.strip():
                packet: Packet = eval(line)
                packets.append(packet)
    return packets


def compare_packet(left: Packet | None, right: Packet | None) -> int:
    if not left and right:
        return -1
    if left and not right:
        return 1
    if isinstance(left, int) and isinstance(right, int):
        return (left > right) - (left < right)
    if isinstance(left, int) and isinstance(right, list):
        return compare_packet([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return compare_packet(left, [right])
    if isinstance(left, list) and isinstance(right, list):
        for left_value, right_value in zip_longest(left, right):
            if result := compare_packet(left_value, right_value):
                return result
    return 0


def part_one(data: list[Packet]) -> int:
    return sum(
        [
            idx
            for idx, (left, right) in enumerate(zip(data[::2], data[1::2]), start=1)
            if compare_packet(left, right) == -1
        ]
    )


def part_two(data: list[Packet]) -> int:
    data.extend([[[2]], [[6]]])
    sorted_data = sorted(data, key=cmp_to_key(compare_packet))
    return (sorted_data.index([[2]]) + 1) * (sorted_data.index([[6]]) + 1)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/13"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 13
    assert part_two(samples) == 140

    print(part_one(data))
    print(part_two(data))
