# https://adventofcode.com/2021/day/10

from collections import deque
from pathlib import Path
from statistics import median


OPENING_BRACKETS = (
    "(",
    "[",
    "{",
    "<",
)
PAIRS = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}
ERROR_SCORING = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
AUTOCOMPLETION_SCORING = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def load_data(path):
    with open(path) as fd:
        return fd.read().splitlines()


def get_scores(lines):
    total_error_score = 0
    autocompletion_scores = []
    for line in lines:
        stack = deque()
        for bracket in line:
            if bracket in OPENING_BRACKETS:
                stack.append(bracket)
            else:
                opening_bracket = stack.pop()
                if opening_bracket != PAIRS[bracket]:
                    total_error_score += ERROR_SCORING[bracket]
                    break
        else:
            score = 0
            while stack:
                score = score * 5 + AUTOCOMPLETION_SCORING[stack.pop()]
            autocompletion_scores.append(score)
    return total_error_score, median(autocompletion_scores)


def part_one(data):
    total_error_score, _ = get_scores(data)
    return total_error_score


def part_two(data):
    _, autocompletion_score = get_scores(data)
    return autocompletion_score


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/10"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 26397
    assert part_two(samples) == 288957

    print(part_one(data))
    print(part_two(data))
