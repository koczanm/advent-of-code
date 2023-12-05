# https://adventofcode.com/2021/day/21

from __future__ import annotations

import abc
from functools import cache
from itertools import cycle, islice, product
from pathlib import Path
from typing import Iterator


class Dice(abc.ABC):
    def __init__(self, sides: int, rolls_per_turn: int) -> None:
        self.sides = sides
        self.rolls_per_turn = rolls_per_turn

    @abc.abstractmethod
    def gen_all_rolls(self) -> Iterator[tuple[int, ...]]:
        pass


class DeterministicDice(Dice):
    def gen_all_rolls(self) -> Iterator[tuple[int, ...]]:
        all_rolls = cycle(range(1, self.sides + 1))
        while True:
            rolls_in_turn = islice(all_rolls, self.rolls_per_turn)
            yield tuple(rolls_in_turn)


class DiracDice(Dice):
    def __init__(self, sides: int) -> None:
        super().__init__(sides, sides)

    def gen_all_rolls(self) -> Iterator[tuple[int, ...]]:
        all_rolls = product(range(1, self.sides + 1), repeat=self.rolls_per_turn)
        for rolls_in_turn in all_rolls:
            yield rolls_in_turn


def load_data(path: Path) -> tuple[int, int]:
    with open(path) as fd:
        player1, player2 = fd.readlines()
    player1_position = int(player1.split(": ")[1])
    player2_position = int(player2.split(": ")[1])
    return player1_position, player2_position


def move(position: int, moves: int) -> int:
    return (position + moves) % 10 or 10


def play_simply(
    player1_position: int,
    player2_position: int,
    dice: DeterministicDice,
    threshold: int = 1000,
) -> tuple[list[int], int]:
    positions = [player1_position, player2_position]
    scores = [0, 0]
    total_rolls = 0
    player_index = 0
    for rolls_in_turn in dice.gen_all_rolls():
        total_rolls += len(rolls_in_turn)
        moves = sum(rolls_in_turn)
        positions[player_index] = move(positions[player_index], moves)
        scores[player_index] += positions[player_index]
        if any(score >= threshold for score in scores):
            break
        player_index = not player_index
    return scores, total_rolls


@cache
def play_dirac(
    player1_position: int,
    player2_position: int,
    dice: DiracDice,
    player1_score: int = 0,
    player2_score: int = 0,
    threshold: int = 21,
) -> tuple[int, int]:
    player1_wins = 0
    player2_wins = 0
    for rolls_in_turn in dice.gen_all_rolls():
        moves = sum(rolls_in_turn)
        player1_new_position = move(player1_position, moves)
        player1_new_score = player1_score + player1_new_position
        if player1_new_score >= threshold:
            player1_wins += 1
        else:
            player2_new_wins, player1_new_wins = play_dirac(
                player2_position,
                player1_new_position,
                dice,
                player2_score,
                player1_new_score,
            )
            player1_wins += player1_new_wins
            player2_wins += player2_new_wins
    return player1_wins, player2_wins


def part_one(data: tuple[int, int]) -> int:
    dice = DeterministicDice(100, 3)
    scores, total_rolls = play_simply(*data, dice)
    return min(scores) * total_rolls


def part_two(data: tuple[int, int]) -> int:
    dice = DiracDice(3)
    wins = play_dirac(*data, dice)
    return max(wins)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/21"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 739785
    assert part_two(samples) == 444356092776315

    print(part_one(data))
    print(part_two(data))
