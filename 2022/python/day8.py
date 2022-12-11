# https://adventofcode.com/2022/day/8

import os
from abc import ABC, abstractproperty
from functools import cached_property
from pathlib import Path
from typing import List, NamedTuple, Union


class Obstacle(NamedTuple):
    height: int
    coord: int


class TreeMap:
    OUTSIDE_HEIGHT: int = 10

    size: int
    trees: List[List["Inner"]]

    def __init__(self, data: List[List[int]]) -> None:
        self.size = len(data)
        self.trees = [[] for _ in range(self.size)]
        self._parse_data(data)

    def get_tree(self, x: int, y: int) -> "Inner":
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.trees[y][x]
        return self.Tree(self.OUTSIDE_HEIGHT, x, y)

    def _parse_data(self, data: List[List[int]]):
        for y, row in enumerate(data):
            for x, height in enumerate(row):
                self.trees[y].append(self.Tree(height, x, y))

    class Inner(ABC):
        height: int
        x: int
        y: int

        @abstractproperty
        def upper_obstacle(self) -> Obstacle:
            raise NotImplementedError()

        @abstractproperty
        def right_obstacle(self) -> Obstacle:
            raise NotImplementedError()

        @abstractproperty
        def lower_obstacle(self) -> Obstacle:
            raise NotImplementedError()

        @abstractproperty
        def left_obstacle(self) -> Obstacle:
            raise NotImplementedError()

        @abstractproperty
        def is_visible(self) -> bool:
            raise NotImplementedError()

        def get_scenic_score(self) -> int:
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
            def upper_obstacle(self) -> Obstacle:
                tree_up = self.tree_map.get_tree(self.x, self.y - 1)
                while tree_up.height < self.height:
                    tree_up = self.tree_map.get_tree(self.x, tree_up.upper_obstacle.coord)
                return Obstacle(tree_up.height, tree_up.y)

            @cached_property
            def right_obstacle(self) -> Obstacle:
                tree_right = self.tree_map.get_tree(self.x + 1, y)
                while tree_right.height < self.height:
                    tree_right = self.tree_map.get_tree(tree_right.right_obstacle.coord, self.y)
                return Obstacle(tree_right.height, tree_right.x)

            @cached_property
            def lower_obstacle(self) -> Obstacle:
                tree_down = self.tree_map.get_tree(self.x, self.y + 1)
                while tree_down.height < self.height:
                    tree_down = self.tree_map.get_tree(self.x, tree_down.lower_obstacle.coord)
                return Obstacle(tree_down.height, tree_down.y)

            @cached_property
            def left_obstacle(self) -> Obstacle:
                tree_left = self.tree_map.get_tree(self.x - 1, self.y)
                while tree_left.height < self.height:
                    tree_left = self.tree_map.get_tree(tree_left.left_obstacle.coord, self.y)
                return Obstacle(tree_left.height, tree_left.x)

            @property
            def is_visible(self) -> bool:
                return any(
                    obstacle.height == self.tree_map.OUTSIDE_HEIGHT
                    for obstacle in (self.upper_obstacle, self.right_obstacle, self.lower_obstacle, self.left_obstacle)
                )

            def get_scenic_score(self) -> int:
                return (
                    (self.y - max(0, self.upper_obstacle.coord))
                    * (min(self.tree_map.size - 1, self.right_obstacle.coord) - self.x)
                    * (min(self.tree_map.size - 1, self.lower_obstacle.coord) - self.y)
                    * (self.x - max(0, self.left_obstacle.coord))
                )

        return _Tree(height, x, y)


def load_data(path: Union[str, bytes, os.PathLike]) -> List[List[int]]:
    with open(path) as fd:
        return [[int(value) for value in row.strip()] for row in fd]


def part_one(data: List[List[int]]) -> int:
    tree_map = TreeMap(data)
    return sum([tree.is_visible for row in tree_map.trees for tree in row])


def part_two(data: List[List[int]]) -> int:
    tree_map = TreeMap(data)
    return max(tree.get_scenic_score() for row in tree_map.trees for tree in row)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/08"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 21
    assert part_two(samples) == 8

    print(part_one(data))
    print(part_two(data))
