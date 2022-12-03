# https://adventofcode.com/2022/day/2

import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

SHAPE_MAPPING: Dict[str, str] = {
    "X": "A",
    "Y": "B",
    "Z": "C",
}

OUTCOME_MAPPING: Dict[str, int] = {
    "X": 0,  # lost
    "Y": 1,  # draw
    "Z": 2,  # win
}

SHAPE_SCORING: Dict[str, int] = {
    "A": 1,
    "B": 2,
    "C": 3,
}

OUTCOME_SCORING: Dict[str, Tuple[str, str, str]] = {
    "A": ("C", "A", "B"),  # in order: lost, draw, win
    "B": ("A", "B", "C"),
    "C": ("B", "C", "A"),
}


def load_data(path: Union[str, bytes, os.PathLike]) -> List[Tuple[str, str]]:
    with open(path) as fd:
        return [tuple(line.split()) for line in fd.readlines()]


def get_total_score(rounds: List[Tuple[str, str]]) -> int:
    total_score = 0
    for opp_shape, my_shape in rounds:
        round_score = SHAPE_SCORING[my_shape]
        round_score += 3 * OUTCOME_SCORING[opp_shape].index(my_shape)
        total_score += round_score
    return total_score


def part_one(data: List[Tuple[str, str]]) -> int:
    rounds = []
    for x, y in data:
        rounds.append((x, SHAPE_MAPPING[y]))
    return get_total_score(rounds)


def part_two(data: List[Tuple[str, str]]) -> int:
    rounds = []
    for x, y in data:
        rounds.append((x, OUTCOME_SCORING[x][OUTCOME_MAPPING[y]]))
    return get_total_score(rounds)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/02"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 15
    assert part_two(samples) == 12

    print(part_one(data))
    print(part_two(data))
