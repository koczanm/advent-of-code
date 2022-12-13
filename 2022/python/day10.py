# https://adventofcode.com/2022/day/10

import os
import re
import textwrap
from pathlib import Path
from typing import List, NamedTuple, Optional, Tuple, Union


class CpuInstr(NamedTuple):
    type_: str
    value: Optional[int] = None


def load_data(path: Union[str, bytes, os.PathLike]) -> List[CpuInstr]:
    cpu_instrs = []
    with open(path) as fd:
        for line in fd:
            cpu_instrs.append(CpuInstr("noop"))
            if match := re.search(r"addx ([^\s]+)", line):
                cpu_instrs.append(CpuInstr("addx", int(match.group(1))))
    return cpu_instrs


def execute(cpu_instrs: List[CpuInstr], wanted_cycles: List[int]) -> int:
    x = 1
    signal_strengths = 0
    for cycle_num, instr in enumerate(cpu_instrs, start=1):
        if cycle_num in wanted_cycles:
            signal_strengths += x * cycle_num
        if instr.type_ == "addx":
            x += instr.value  # type: ignore
    return signal_strengths


def draw(cpu_instrs: List[CpuInstr]) -> str:
    x = 1
    crt = ""
    for cycle_num, instr in enumerate(cpu_instrs, start=1):
        pixel = (cycle_num - 1) % 40
        if x - 1 <= pixel <= x + 1:
            crt += "#"
        else:
            crt += "."
        if pixel == 39:
            crt += "\n"
        if instr.type_ == "addx":
            x += instr.value  # type: ignore
    return crt


def part_one(data: List[CpuInstr]) -> int:
    wanted_cycles = [20, 60, 100, 140, 180, 220]
    signal_strengths = execute(data, wanted_cycles)
    return signal_strengths


def part_two(data: List[CpuInstr]) -> str:
    crt = draw(data)
    return crt


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/10"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 13140
    assert part_two(samples) == textwrap.dedent(
        """\
        ##..##..##..##..##..##..##..##..##..##..
        ###...###...###...###...###...###...###.
        ####....####....####....####....####....
        #####.....#####.....#####.....#####.....
        ######......######......######......####
        #######.......#######.......#######.....
    """
    )

    print(part_one(data))
    print(part_two(data))
