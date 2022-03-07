# https://adventofcode.com/2021/day/18

import copy
import math
import operator
from functools import reduce
from itertools import permutations
from pathlib import Path


class SnailfishNumber:
    def __init__(self, value=None, parent=None, left=None, right=None):
        self.value = value
        self.parent = parent
        self.left = left
        if left is not None:
            left.parent = self
        self.right = right
        if right is not None:
            right.parent = self

    def __add__(self, other):
        left = copy.deepcopy(self)
        right = copy.deepcopy(other)
        return SnailfishNumber(left=left, right=right).reduce()

    def __repr__(self):
        if self.value is None:
            return f'[{repr(self.left)}, {repr(self.right)}]'
        return repr(self.value)

    def __find_explosion_candidate(self, depth=0):
        if self.value is None:
            if depth < 4:
                depth += 1
                return self.left.__find_explosion_candidate(depth) or self.right.__find_explosion_candidate(depth)
            return self
        return None

    def __find_split_candidate(self):
        if self.value is None:
            return self.left.__find_split_candidate() or self.right.__find_split_candidate()
        return self if self.value >= 10 else None

    def __explode(self):
        current = self
        while current.parent and current.parent.left == current:
            current = current.parent
        if current.parent:
            current = current.parent.left
            while current.value is None:
                current = current.right
            current.value += self.left.value
        current = self
        while current.parent and current.parent.right == current:
            current = current.parent
        if current.parent:
            current = current.parent.right
            while current.value is None:
                current = current.left
            current.value += self.right.value
        self.left = None
        self.right = None
        self.value = 0

    def __split(self):
        self.left = SnailfishNumber(value=math.floor(self.value / 2), parent=self)
        self.right = SnailfishNumber(value=math.ceil(self.value / 2), parent=self)
        self.value = None

    @property
    def magnitude(self):
        if self.value is None:
            return 3 * self.left.magnitude + 2 * self.right.magnitude
        return self.value

    def reduce(self):
        while True:
            if (number := self.__find_explosion_candidate()) is not None:
                number.__explode()
            elif (number := self.__find_split_candidate()) is not None:
                number.__split()
            else:
                break
        return self

    @staticmethod
    def eval(input_str):
        root = SnailfishNumber()
        current = root
        for char in input_str:
            match char:
                case '[':
                    current.left = SnailfishNumber(parent=current)
                    current.right = SnailfishNumber(parent=current)
                    current = current.left
                case ']':
                    current = current.parent
                case ',':
                    current = current.parent.right
                case _:
                    current.value = int(char)
        return root


def load_data(path):
    with open(path) as fd:
        return [SnailfishNumber.eval(line.strip()) for line in fd]


def part_one(data):
    result = reduce(operator.add, data)
    return result.magnitude


def part_two(data):
    max_magnitude = 0
    for a, b in permutations(data, 2):
        result = a + b
        max_magnitude = max(max_magnitude, result.magnitude)
    return max_magnitude


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/18"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 4140
    assert part_two(samples) == 3993

    print(part_one(data))
    print(part_two(data))
