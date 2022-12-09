# https://adventofcode.com/2022/day/8

import os
from abc import ABC, abstractproperty
from functools import cached_property
from pathlib import Path
from typing import List, Union


class TreeMap:
    trees: List[List["Inner"]]

    def __init__(self, data: List[List[int]]) -> None:
        self.size = len(data)
        self.trees = [[] for _ in range(self.size)]
        self._parse_data(data)

    def _parse_data(self, data: List[List[int]]):
        for y, row in enumerate(data):
            for x, height in enumerate(row):
                self.trees[y].append(self.Tree(height, x, y))

    class Inner(ABC):
        height: int
        x: int
        y: int

        @abstractproperty
        def max_height_up(self) -> bool:
            raise NotImplementedError()

        @abstractproperty
        def max_height_right(self) -> bool:
            raise NotImplementedError()

        @abstractproperty
        def max_height_down(self) -> bool:
            raise NotImplementedError()

        @abstractproperty
        def max_height_left(self) -> bool:
            raise NotImplementedError()

        @abstractproperty
        def is_visible(self) -> bool:
            raise NotImplementedError()

    def Tree(self, height: int, x: int, y: int) -> Inner:
        tree_map = self

        class _Tree(TreeMap.Inner):
            def __init__(self, height: int, x: int, y: int) -> None:
                self.height = height
                self.tree_map = tree_map
                self.x = x
                self.y = y

            @cached_property
            def max_height_up(self) -> int:
                if self.y == 0:
                    return -1
                tree_up = self.tree_map.trees[self.y - 1][self.x]
                return max(tree_up.height, tree_up.max_height_up)

            @cached_property
            def max_height_right(self) -> int:
                if self.x == self.tree_map.size - 1:
                    return -1
                tree_right = self.tree_map.trees[self.y][self.x + 1]
                return max(tree_right.height, tree_right.max_height_right)

            @cached_property
            def max_height_down(self) -> int:
                if self.y == self.tree_map.size - 1:
                    return -1
                tree_down = self.tree_map.trees[self.y + 1][self.x]
                return max(tree_down.height, tree_down.max_height_down)

            @cached_property
            def max_height_left(self) -> int:
                if self.x == 0:
                    return -1
                tree_left = self.tree_map.trees[self.y][self.x - 1]
                return max(tree_left.height, tree_left.max_height_left)

            @property
            def is_visible(self) -> bool:
                return any(
                    max_height < self.height
                    for max_height in (
                        self.max_height_up,
                        self.max_height_right,
                        self.max_height_down,
                        self.max_height_left,
                    )
                )

        return _Tree(height, x, y)


def load_data(path: Union[str, bytes, os.PathLike]) -> List[List[int]]:
    with open(path) as fd:
        return [[int(value) for value in row.strip()] for row in fd]


def part_one(data: List[List[int]]) -> int:
    tree_map = TreeMap(data)
    return sum([tree.is_visible for row in tree_map.trees for tree in row])


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/08"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 21

    print(part_one(data))
