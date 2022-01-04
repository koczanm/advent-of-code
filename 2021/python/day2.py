# https://adventofcode.com/2021/day/2

from pathlib import Path


def load_data(path):
    data = []
    with open(path) as fd:
        for line in fd:
            direction, value = line.split()
            data.append((direction, int(value)))
    return data


def follow_course(cmds):
    h_pos = 0
    depth = 0
    aim = 0
    for direction, value in cmds:
        if direction == "forward":
            h_pos += value
            depth += value * aim
        elif direction == "down":
            aim += value
        else:
            aim -= value
    return h_pos, depth, aim


def part_one(data):
    h_pos, _, depth = follow_course(data)
    return h_pos * depth


def part_two(data):
    h_pos, depth, _ = follow_course(data)
    return h_pos * depth


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/02"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    h_pos, depth, aim = follow_course(samples)
    assert h_pos * aim == 150
    assert h_pos * depth == 900

    h_pos, depth, aim = follow_course(data)
    print(part_one(data))
    print(part_two(data))
