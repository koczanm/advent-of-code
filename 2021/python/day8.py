# https://adventofcode.com/2021/day/8

from collections import defaultdict
from pathlib import Path


DIGIT_TO_LENGTH = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6
}


def load_data(path):
    data = []
    with open(path) as fd:
        for line in fd:
            patterns, output = line.split("|")
            patterns = [frozenset(pattern) for pattern in patterns.split()]
            output = [frozenset(output) for output in output.split()]
            data.append((patterns, output))
    return data


def get_first_match(criteria, candidates):
    return next(filter(criteria, candidates))


def determine_mapping(patterns):
    digits = {}
    candidates = defaultdict(list)
    for pattern in patterns:
        candidates[len(pattern)].append(pattern)

    digits[1] = candidates[DIGIT_TO_LENGTH[1]][0]
    digits[4] = candidates[DIGIT_TO_LENGTH[4]][0]
    digits[7] = candidates[DIGIT_TO_LENGTH[7]][0]
    digits[8] = candidates[DIGIT_TO_LENGTH[8]][0]
    digits[3] = get_first_match(lambda c: digits[1].issubset(c), candidates[DIGIT_TO_LENGTH[3]])
    digits[9] = get_first_match(lambda c: digits[4].issubset(c), candidates[DIGIT_TO_LENGTH[9]])
    digits[0] = get_first_match(lambda c: c != digits[9] and digits[1].issubset(c), candidates[DIGIT_TO_LENGTH[0]])
    digits[6] = get_first_match(lambda c: c not in [digits[0], digits[9]], candidates[DIGIT_TO_LENGTH[6]])
    digits[5] = get_first_match(lambda c: c.issubset(digits[6]), candidates[DIGIT_TO_LENGTH[5]])
    digits[2] = get_first_match(lambda c: c not in [digits[3], digits[5]], candidates[DIGIT_TO_LENGTH[2]])

    return {pattern: digit for digit, pattern in digits.items()}


def part_one(data):
    wanted_digits = [1, 4, 7, 8]
    result = 0
    for patterns, output in data:
        patterns_to_digits = determine_mapping(patterns)
        for o in output:
            if patterns_to_digits[o] in wanted_digits:
                result += 1
    return result


def part_two(data):
    result = 0
    for patterns, output in data:
        patterns_to_digits = determine_mapping(patterns)
        for i, factor in enumerate((1000, 100, 10, 1)):
            result += patterns_to_digits[output[i]] * factor
    return result


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/08"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 26
    assert part_two(samples) == 61229

    print(part_one(data))
    print(part_two(data))

