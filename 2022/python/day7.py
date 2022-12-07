# https://adventofcode.com/2022/day/6

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union


class File(NamedTuple):
    name: str
    size: int


class Dir:
    parent: Optional[Dir]
    subdirs: Dict[str, Dir]
    files: List[File]

    def __init__(self, parent: Optional[Dir] = None) -> None:
        self.parent = parent
        self.subdirs = {}
        self.files = []

    def make_dir(self, name: str) -> None:
        self.subdirs[name] = Dir(self)

    def create_file(self, name: str, size: int) -> None:
        self.files.append(File(name, size))

    def cd(self, name: str) -> Dir:
        if name == "/":
            return self.parent.cd("/") if self.parent else self
        elif name == "..":
            return self.parent if self.parent else self
        return self.subdirs[name]

    def get_total_size(self) -> int:
        return sum(d.get_total_size() for d in self.subdirs.values()) + sum(f.size for f in self.files)

    def find_dirs(self, maxsize: int = 100000) -> List[Dir]:
        dirs = []
        for d in self.subdirs.values():
            dirs.extend(d.find_dirs(maxsize))
        if self.get_total_size() <= maxsize:
            dirs.append(self)
        return dirs


def load_data(path: Union[str, bytes, os.PathLike]) -> Dir:
    curr_dir = Dir()
    with open(path) as fd:
        for line in fd:
            if match := re.search(r"\$ cd ([^\s]+)", line):
                curr_dir = curr_dir.cd(match.group(1))
            elif match := re.search(r"dir ([^\s]+)", line):
                curr_dir.make_dir(match.group(1))
            elif match := re.search(r"(\d+) ([^\s]+)", line):
                curr_dir.create_file(match.group(2), int(match.group(1)))
            else:
                continue
    return curr_dir.cd("/")


def part_one(data: Dir) -> int:
    return sum(d.get_total_size() for d in data.find_dirs())


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/07"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 95437

    print(part_one(data))
