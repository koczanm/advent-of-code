# https://adventofcode.com/2021/day/4

import copy
from collections import defaultdict
from pathlib import Path


class BingoBoard:
    SIZE = 5

    def __init__(self, data):
        self._bingo = False
        self._row_counter = defaultdict(int)
        self._col_counter = defaultdict(int)
        self._numbers = defaultdict(list)
        for row, line in enumerate(data.split("\n")):
            for col, number in enumerate(line.split()):
                self._numbers[int(number)].append((row, col))

    @property
    def is_bingo(self):
        return self._bingo

    def mark(self, number):
        for row, col in self._numbers.pop(number, []):
            self._row_counter[row] += 1
            self._col_counter[col] += 1
            if self._row_counter[row] == self.SIZE or self._col_counter[col] == self.SIZE:
                self._bingo = True

    def sum_unmarked(self):
        return sum(self._numbers.keys())


def load_data(path):
    with open(path) as fd:
        numbers, *boards = fd.read().split("\n\n")
    numbers = [int(number) for number in numbers.split(",")]
    boards = [BingoBoard(board) for board in boards]
    return numbers, boards


def play(numbers, boards, to_end=False):
    boards = copy.deepcopy(boards)
    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.is_bingo:
                if not to_end:
                    return number * board.sum_unmarked()
                elif len(boards) == 1:
                    return number * board.sum_unmarked()
        boards = [board for board in boards if not board.is_bingo]


def part_one(data):
    return play(*data)


def part_two(data):
    return play(*data, to_end=True)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/04/"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 4512
    assert part_two(samples) == 1924

    print(part_one(data))
    print(part_two(data))
