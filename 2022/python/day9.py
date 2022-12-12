# https://adventofcode.com/2022/day/9

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set, Tuple, Union


@dataclass(eq=True, frozen=True)
class Position:
    x: int
    y: int

    def adjacents(self, other: Position) -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1


@dataclass
class Motion:
    direction: str
    steps_num: int


def load_data(path: Union[str, bytes, os.PathLike]) -> List[Motion]:
    motions = []
    with open(path) as fd:
        for line in fd:
            direction, steps_num = line.split()
            motions.append(Motion(direction, int(steps_num)))
    return motions


def move_knot(dest: Position, knot: Position) -> Position:
    while not knot.adjacents(dest):
        dx, dy = dest.x - knot.x, dest.y - knot.y
        if dx == 0:
            nx, ny = knot.x, knot.y + dy // abs(dy)
        elif dy == 0:
            nx, ny = knot.x + dx // abs(dx), knot.y
        else:
            nx, ny = knot.x + dx // abs(dx), knot.y + dy // abs(dy)
        knot = Position(nx, ny)
    return knot


def simulate(motions: List[Motion], rope: List[Position]) -> Set[Position]:
    all_visited = {rope[-1]}
    for motion in motions:
        for _ in range(motion.steps_num):
            head, *rest_knots = rope
            match motion.direction:
                case "U":
                    head = Position(head.x, head.y + 1)
                case "D":
                    head = Position(head.x, head.y - 1)
                case "L":
                    head = Position(head.x - 1, head.y)
                case "R":
                    head = Position(head.x + 1, head.y)
            rope = [head]
            for knot in rest_knots:
                knot = move_knot(rope[-1], knot)
                rope.append(knot)
            all_visited.add(rope[-1])
    return all_visited


def part_one(data: List[Motion]) -> int:
    rope = [Position(0, 0) for _ in range(2)]
    visited = simulate(data, rope)
    return len(visited)


def part_two(data: List[Motion]) -> int:
    rope = [Position(0, 0) for _ in range(10)]
    visited = simulate(data, rope)
    return len(visited)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/09"
    samples1 = load_data(input_dir / "samples1.in")
    samples2 = load_data(input_dir / "samples2.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples1) == 13
    assert part_two(samples1) == 1
    assert part_two(samples2) == 36

    print(part_one(data))
    print(part_two(data))
