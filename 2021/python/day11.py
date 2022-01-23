# https://adventofcode.com/2021/day/11

import copy
from collections import deque
from itertools import product
from pathlib import Path


class Octopuses(object):
    def __init__(self, energy_levels):
        self.energy_levels = copy.deepcopy(energy_levels)
        self.rows_num = len(energy_levels)
        self.cols_num = len(energy_levels[0])
        self.steps_num = 0

    def _increase_energy(self):
        for y in range(self.rows_num):
            for x in range(self.cols_num):
                self.energy_levels[y][x] += 1

    def _get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in product((-1, 0, 1), repeat=2):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols_num and 0 <= ny < self.rows_num:
                neighbors.append((nx, ny))
        return neighbors

    def do_step(self):
        self.steps_num += 1
        self._increase_energy()
        flashing_octopuses = deque()
        for y, row in enumerate(self.energy_levels):
            for x, energy_level in enumerate(row):
                if energy_level > 9:
                    flashing_octopuses.append((x, y))
        flashes = 0
        while flashing_octopuses:
            flashes += 1
            x, y = flashing_octopuses.popleft()
            self.energy_levels[y][x] = 0
            for nx, ny in self._get_neighbors(x, y):
                if 0 < self.energy_levels[ny][nx] <= 9:
                    self.energy_levels[ny][nx] += 1
                    if self.energy_levels[ny][nx] > 9:
                        flashing_octopuses.append((nx, ny))
        return flashes

    def simulate(self, steps_num):
        flashes = 0
        while self.steps_num < steps_num:
            flashes += self.do_step()
        return flashes

    def simulate_until_all_flash(self):
        all_flashed = self.rows_num * self.cols_num
        flashes = 0
        while flashes < all_flashed:
            flashes = self.do_step()
        return self.steps_num


def load_data(path):
    with open(path) as fd:
        return [[int(x) for x in line.strip()] for line in fd]


def part_one(data):
    octopuses = Octopuses(data)
    return octopuses.simulate(steps_num=100)


def part_two(data):
    octopuses = Octopuses(data)
    return octopuses.simulate_until_all_flash()


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/11"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 1656
    assert part_two(samples) == 195

    print(part_one(data))
    print(part_two(data))
