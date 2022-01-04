# https://adventofcode.com/2021/day/1

from pathlib import Path


def load_data(path):
    with open(path) as fp:
        return [int(line) for line in fp]


def count_increasing_depth_num(measurements, sliding_window_size=1):
    return sum(x < y for x, y in zip(measurements, measurements[sliding_window_size:]))


def part_one(data):
    return count_increasing_depth_num(data)


def part_two(data):
    return count_increasing_depth_num(data, 3)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/01"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 7
    assert part_two(samples) == 5

    print(part_one(data))
    print(part_two(data))
