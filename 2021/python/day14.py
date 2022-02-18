# https://adventofcode.com/2021/day/14

from collections import Counter
from functools import cache
from pathlib import Path


def load_data(path):
    with open(path) as fd:
        template, _, *rules = fd.read().splitlines()
        rules = {k: v for k, v in (rule.split(" -> ") for rule in rules)}
        return template, rules


def polymerize(template, rules, steps_num):
    @cache
    def count(pair, step):
        if step == steps_num or pair not in rules:
            return Counter()
        step += 1
        pair_ins = rules[pair]
        new_counter = Counter(pair_ins)
        new_counter.update(count(pair[0] + pair_ins, step))
        new_counter.update(count(pair_ins + pair[1], step))
        return new_counter

    counter = Counter(template)
    for left, right in zip(template[0:], template[1:]):
        counter.update(count(left + right, 0))
    return counter


def get_diff(counter):
    sorted_by_quantity = counter.most_common()
    return sorted_by_quantity[0][1] - sorted_by_quantity[-1][1]


def part_one(data):
    return get_diff(polymerize(*data, 10))


def part_two(data):
    return get_diff(polymerize(*data, 40))


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/14"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 1588
    assert part_two(samples) == 2188189693529

    print(part_one(data))
    print(part_two(data))
