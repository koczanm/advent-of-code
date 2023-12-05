# https://adventofcode.com/2023/day/1

import os
from pathlib import Path

NUM_WORDS = {
    "one": "one1one",
    "two": "two2two",
    "three": "three3three",
    "four": "four4four",
    "five": "five5five",
    "six": "six6six",
    "seven": "seven7seven",
    "eight": "eight8eight",
    "nine": "nine9nine",
}


def load_data(path: str | bytes | os.PathLike) -> list[str]:
    with open(path) as fd:
        return fd.readlines()


def find_calibration_num(line: str, convert_num_words: bool = False) -> int:
    if convert_num_words:
        for word, num in NUM_WORDS.items():
            line = line.replace(word, num)
    digits = [char for char in line if char.isdigit()]
    return int(digits[0] + digits[-1])


def part_one(data: list[str]) -> int:
    return sum(find_calibration_num(line) for line in data)


def part_two(data: list[str]) -> int:
    return sum(find_calibration_num(line, convert_num_words=True) for line in data)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/01"
    samples1 = load_data(input_dir / "samples1.in")
    samples2 = load_data(input_dir / "samples2.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples1) == 142
    assert part_two(samples2) == 281

    print(part_one(data))
    print(part_two(data))
