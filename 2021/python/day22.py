# https://adventofcode.com/2021/day/22

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Union


class CoordRange:
    def __init__(self, begin: int, end: int) -> None:
        self.begin = begin
        self.end = end

    def __contains__(self, item: Union[int, CoordRange]) -> bool:
        if isinstance(item, int):
            return self.begin <= item < self.end
        return self.begin <= item.begin and self.end >= item.end

    def __len__(self) -> int:
        return self.end - self.begin

    def __repr__(self) -> str:
        return f"CoordRange({self.begin}, {self.end})"

    def intersection(self, other: CoordRange) -> Optional[CoordRange]:
        if self.begin < other.end and self.end > other.begin:
            begin = max(self.begin, other.begin)
            end = min(self.end, other.end)
            return CoordRange(begin, end)
        return None


class Cuboid:
    def __init__(self, x_range: CoordRange, y_range: CoordRange, z_range: CoordRange, is_on: bool = False) -> None:
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.is_on = is_on

    def __contains__(self, item: Union[int, Cuboid]) -> bool:
        if isinstance(item, int):
            return item in self.x_range and item in self.y_range and item in self.z_range
        return item.x_range in self.x_range and item.y_range in self.y_range and item.z_range in self.z_range

    def __repr__(self) -> str:
        return f"Cuboid({repr(self.x_range)}, {repr(self.y_range)}, {repr(self.z_range)})"

    @property
    def volume(self) -> int:
        v = len(self.x_range) * len(self.y_range) * len(self.z_range)
        return v if self.is_on else -v

    def intersection(self, other: Cuboid) -> Optional[Cuboid]:
        if (
            (x_range := self.x_range.intersection(other.x_range)) is not None
            and (y_range := self.y_range.intersection(other.y_range)) is not None
            and (z_range := self.z_range.intersection(other.z_range)) is not None
        ):
            return Cuboid(x_range, y_range, z_range, not self.is_on)
        return None


def load_data(path: Path) -> list[Cuboid]:
    cuboids = []
    with open(path) as fd:
        for line in fd:
            is_on = line.startswith("on")
            x_min, x_max, y_min, y_max, z_min, z_max = [int(coord) for coord in re.findall(r"-?\d+", line)]
            x_range = CoordRange(x_min, x_max + 1)
            y_range = CoordRange(y_min, y_max + 1)
            z_range = CoordRange(z_min, z_max + 1)
            cuboids.append(Cuboid(x_range, y_range, z_range, is_on))
    return cuboids


def find_intersections(cuboid: Cuboid, candidates: list[Cuboid]) -> list[Cuboid]:
    cuboids = []
    for candidate in candidates:
        intersection = candidate.intersection(cuboid)
        if intersection:
            cuboids.append(intersection)
    return cuboids


def apply_init_procedure(cuboids: list[Cuboid], region: Cuboid) -> list[Cuboid]:
    return [cuboid for cuboid in cuboids if cuboid in region]


def reboot_reactor(cuboids: list[Cuboid]) -> int:
    processed_cuboids = []
    for cuboid in cuboids:
        intersections = find_intersections(cuboid, processed_cuboids)
        processed_cuboids.extend(intersections)
        if cuboid.is_on:
            processed_cuboids.append(cuboid)
    return sum(cuboid.volume for cuboid in processed_cuboids)


def part_one(data: list[Cuboid]) -> int:
    border = CoordRange(-50, 51)
    region = Cuboid(border, border, border)
    bounded_cuboids = apply_init_procedure(data, region)
    return reboot_reactor(bounded_cuboids)


def part_two(data: list[Cuboid]) -> int:
    return reboot_reactor(data)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/22"
    samples1 = load_data(input_dir / "samples1.in")
    samples2 = load_data(input_dir / "samples2.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples1) == 590784
    assert part_two(samples2) == 2758514936282235

    print(part_one(data))
    print(part_two(data))
