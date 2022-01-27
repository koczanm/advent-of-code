# https://adventofcode.com/2021/day/13

from collections import namedtuple
from pathlib import Path


Dot = namedtuple("Dot", "x y")
Fold = namedtuple("Fold", "axis value")


def load_data(path):
    with open(path) as fd:
        top, bottom = fd.read().split("\n\n")
    paper = set()
    for line in top.splitlines():
        x, y = line.split(",")
        paper.add(Dot(int(x), int(y)))
    fold_instrs = []
    for line in bottom.splitlines():
        instr, value = line.split("=")
        fold_instrs.append(Fold(instr[-1], int(value)))
    return paper, fold_instrs


def fold_vrt(paper, x):
    folded_paper = set()
    for dot in paper:
        if dot.x > x:
            new_dot = Dot(2 * x - dot.x, dot.y)
            folded_paper.add(new_dot)
        elif dot.x < x:
            folded_paper.add(dot)
    return folded_paper


def fold_hor(paper, y):
    folded_paper = set()
    for dot in paper:
        if dot.y > y:
            new_dot = Dot(dot.x, 2 * y - dot.y)
            folded_paper.add(new_dot)
        elif dot.y < y:
            folded_paper.add(dot)
    return folded_paper


def fold(paper, instr):
    if instr.axis == "x":
        return fold_vrt(paper, instr.value)
    else:
        return fold_hor(paper, instr.value)


def print_code(paper):
    width = max(paper, key=lambda dot: dot.x).x + 1
    height = max(paper, key=lambda dot: dot.y).y + 1
    code = [["."] * width for _ in range(height)]
    for dot in paper:
        code[dot.y][dot.x] = "#"
    return "\n".join("".join(line) for line in code)


def part_one(data):
    paper, fold_instrs = data
    paper = fold(paper, fold_instrs[0])
    return len(paper)


def part_two(data):
    paper, fold_instrs = data
    for instr in fold_instrs:
        paper = fold(paper, instr)
    return print_code(paper)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/13"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 17
    part_two(samples) == ("#####\n" "#   #\n" "#   #\n" "#   #\n" "#####\n")

    print(part_one(data))
    print(part_two(data))
