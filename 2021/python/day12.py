# https://adventofcode.com/2021/day/12

from collections import defaultdict
from functools import cache
from pathlib import Path


def load_data(path):
    cave_system = defaultdict(list)
    with open(path) as fd:
        for line in fd:
            a, b = line.strip().split("-")
            cave_system[a].append(b)
            cave_system[b].append(a)
    return cave_system


def count_distinct_paths(cave_system, visit_single_small_twice=False):
    @cache
    def find_next_paths(cave, visited, visit_single_small_twice):
        if cave.islower():
            visited = visited.union({cave})
        distinct_paths = 0
        for next_cave in cave_system[cave]:
            if next_cave == "end":
                distinct_paths += 1
            elif next_cave not in visited:
                distinct_paths += find_next_paths(next_cave, visited, visit_single_small_twice)
            elif next_cave != "start" and visit_single_small_twice:
                distinct_paths += find_next_paths(next_cave, visited, False)
        return distinct_paths

    return find_next_paths("start", frozenset(), visit_single_small_twice)


def part_one(data):
    return count_distinct_paths(data)


def part_two(data):
    return count_distinct_paths(data, True)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/12"
    samples1 = load_data(input_dir / "samples1.in")
    samples2 = load_data(input_dir / "samples2.in")
    samples3 = load_data(input_dir / "samples3.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples1) == 10
    assert part_one(samples2) == 19
    assert part_one(samples3) == 226
    assert part_two(samples1) == 36
    assert part_two(samples2) == 103
    assert part_two(samples3) == 3509

    print(part_one(data))
    print(part_two(data))
