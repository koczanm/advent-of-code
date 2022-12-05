# https://adventofcode.com/2022/day/5

import copy
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple, Union

Stack = List[str]


class Procedure(NamedTuple):
    quantity: int
    src: int
    dest: int


def load_data(path: Union[str, bytes, os.PathLike]) -> Tuple[Dict[int, Stack], List[Procedure]]:
    with open(path) as fd:
        top, bottom = fd.read().split("\n\n")
    stacks = defaultdict(list)
    for line in top.splitlines()[:-1][::-1]:
        for i, crate in enumerate(line[1::4], start=1):
            if crate != " ":
                stacks[i].append(crate)
    procedures = []
    for line in bottom.splitlines():
        proc = Procedure(*[int(x) for x in re.findall(r"\d+", line)])
        procedures.append(proc)
    return stacks, procedures


def rearrange(stacks: Dict[int, Stack], procedures: List[Procedure], reverse: bool = True) -> Dict[int, Stack]:
    stacks = copy.deepcopy(stacks)
    for proc in procedures:
        left_crates, moved_crates = stacks[proc.src][: -proc.quantity], stacks[proc.src][-proc.quantity :]
        stacks[proc.src] = left_crates
        stacks[proc.dest].extend(reversed(moved_crates) if reverse else moved_crates)
    return stacks


def part_one(data: Tuple[Dict[int, Stack], List[Procedure]]) -> str:
    stacks, procedures = data
    rearranged_stacks = rearrange(stacks, procedures)
    return "".join([stack[-1] for stack in rearranged_stacks.values()])


def part_two(data: Tuple[Dict[int, Stack], List[Procedure]]) -> str:
    stacks, procedures = data
    rearranged_stacks = rearrange(stacks, procedures, reverse=False)
    return "".join([stack[-1] for stack in rearranged_stacks.values()])


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/05"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == "CMZ"
    assert part_two(samples) == "MCD"

    print(part_one(data))
    print(part_two(data))
