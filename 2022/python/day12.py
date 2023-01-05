# https://adventofcode.com/2022/day/12

import os
from collections import abc, defaultdict, deque
from pathlib import Path
from typing import Deque, Iterator, NamedTuple, cast

Coord = NamedTuple("Coord", [("x", int), ("y", int)])
Graph = dict[Coord, list[Coord]]

E: int = ord("E")
S: int = ord("S")
a: int = ord("a")
z: int = ord("z")


class PathNotFoundError(Exception):
    pass


class HeightMap(abc.Iterable):
    def __init__(self, data: list[list[int]]) -> None:
        self.data = data
        self.x_max = len(data[0]) - 1
        self.y_max = len(data) - 1

    def __iter__(self) -> Iterator[tuple[int, Coord]]:
        for y, row in enumerate(self.data):
            for x, elev in enumerate(row):
                yield elev, Coord(x, y)

    def get(self, coord: Coord) -> int:
        return self.data[coord.y][coord.x]

    def get_neighbors(self, coord: Coord) -> list[tuple[int, Coord]]:
        x, y = coord
        neighbors = []
        if x > 0:
            ncoord = Coord(x - 1, y)
            neighbors.append((self.get(ncoord), ncoord))
        if x < self.x_max:
            ncoord = Coord(x + 1, y)
            neighbors.append((self.get(ncoord), ncoord))
        if y > 0:
            ncoord = Coord(x, y - 1)
            neighbors.append((self.get(ncoord), ncoord))
        if y < self.y_max:
            ncoord = Coord(x, y + 1)
            neighbors.append((self.get(ncoord), ncoord))
        return neighbors


def load_data(path: str | bytes | os.PathLike) -> HeightMap:
    with open(path) as fd:
        return HeightMap([[ord(elev) for elev in line.strip()] for line in fd])


def build_graph(height_map: HeightMap, find_all_starts: bool = False) -> tuple[Graph, list[Coord], Coord]:
    graph: Graph = defaultdict(list)
    starts = []
    end = None
    for elev, coord in height_map:
        if elev == S:
            elev = a
            starts.append(coord)
        elif elev == E:
            elev = z
            end = coord
        elif find_all_starts and elev == a:
            starts.append(coord)
        for nelev, ncoord in height_map.get_neighbors(coord):
            if nelev == S:
                nelev = ord("a")
            elif nelev == E:
                nelev = ord("z")
            if nelev - elev <= 1:
                graph[coord].append(ncoord)
    end = cast(Coord, end)
    return graph, starts, end


def bfs(graph: Graph, start: Coord, end: Coord) -> list[Coord]:
    visited: set[Coord] = set([start])
    queue: Deque[tuple[Coord, list[Coord]]] = deque([(start, [start])])

    while queue:
        coord, path = queue.popleft()
        for ncoord in graph[coord]:
            if ncoord == end:
                return [*path, ncoord]
            if ncoord not in visited:
                visited.add(ncoord)
                queue.append((ncoord, [*path, ncoord]))
    raise PathNotFoundError(f"No path from {start} to {end}")


def part_one(data: HeightMap) -> int:
    graph, starts, end = build_graph(data)
    path = bfs(graph, starts[0], end)
    return len(path) - 1


def part_two(data: HeightMap) -> int:
    graph, starts, end = build_graph(data, find_all_starts=True)
    paths = []
    for start in starts:
        try:
            path = bfs(graph, start, end)
        except PathNotFoundError:
            continue
        paths.append(path)
    path = min(paths, key=len)
    return len(path) - 1


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/12"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 31
    assert part_two(samples) == 29

    print(part_one(data))
    print(part_two(data))
