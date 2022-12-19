# https://adventofcode.com/2022/day/6

from __future__ import annotations

import copy
import math
import os
import re
from collections import deque
from pathlib import Path
from typing import Callable, Deque, List, NamedTuple, Tuple, Union


class Test(NamedTuple):
    divisor: int
    true: int
    false: int


class Monkey:
    def __init__(self, items: Deque[int], op: str, test: Test) -> None:
        self.items = items
        self.op = op
        self.op_fn = lambda old: eval(op)  # pyright: ignore
        self.test = test
        self.total_items_num = 0

    def __copy__(self) -> Monkey:
        return Monkey(copy.deepcopy(self.items), self.op, self.test)

    def add_item(self, item: int) -> None:
        self.items.append(item)

    def inspect_items(self, worry_fn: Callable[[int], int]) -> List[Tuple[int, int]]:
        self.total_items_num += len(self.items)
        result = []
        while self.items:
            worry_level = self.items.popleft()
            new_worry_level = worry_fn(self.op_fn(worry_level))
            if new_worry_level % self.test.divisor == 0:
                result.append((new_worry_level, self.test.true))
            else:
                result.append((new_worry_level, self.test.false))
        return result


def load_data(path: Union[str, bytes, os.PathLike]) -> List[Monkey]:
    monkeys = []
    with open(path) as fd:
        for raw_monkey in fd.read().split("\n\n"):
            lines = raw_monkey.splitlines()
            items = deque([int(num) for num in re.findall(r"\d+", lines[1])])
            op = lines[2].rsplit("=", maxsplit=1)[-1]
            divider = int(lines[3].rsplit(maxsplit=1)[-1])
            true = int(lines[4].rsplit(maxsplit=1)[-1])
            false = int(lines[5].rsplit(maxsplit=1)[-1])
            monkeys.append(Monkey(items, op, Test(divider, true, false)))
    return monkeys


def play(monkeys: List[Monkey], rounds_num: int, worry_fn: Callable[[int], int]) -> int:
    common_divisor = math.prod([monkey.test.divisor for monkey in monkeys])
    for _ in range(rounds_num):
        for monkey in monkeys:
            for item, monkey_idx in monkey.inspect_items(worry_fn):
                monkeys[monkey_idx].add_item(item % common_divisor)
    most_active_monkeys = sorted(monkeys, key=lambda monkey: monkey.total_items_num)
    monkey_business = most_active_monkeys[-1].total_items_num * most_active_monkeys[-2].total_items_num
    return monkey_business


def part_one(data: List[Monkey]) -> int:
    monkeys = copy.deepcopy(data)
    return play(monkeys, rounds_num=20, worry_fn=lambda worry_level: worry_level // 3)


def part_two(data: List[Monkey]) -> int:
    monkeys = copy.deepcopy(data)
    return play(monkeys, rounds_num=10000, worry_fn=lambda worry_level: worry_level)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/11"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 10605
    assert part_two(samples) == 2713310158

    print(part_one(data))
    print(part_two(data))
