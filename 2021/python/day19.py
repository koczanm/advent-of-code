# https://adventofcode.com/2021/day/19

from __future__ import annotations
from itertools import combinations, product
from math import prod
from pathlib import Path


class InsufficientOverlapError(Exception):
    pass


class Vector3:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other: Vector3) -> bool:
        return isinstance(other, Vector3) and (self.x, self.y, self.z) == (
            other.x,
            other.y,
            other.z,
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def distance_to(self, other: Vector3) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def translate(self, translation: Vector3) -> None:
        self.x += translation.x
        self.y += translation.y
        self.z += translation.z

    def rotate_around_x(self) -> None:
        self.x, self.y, self.z = self.x, -self.z, self.y

    def rotate_around_y(self) -> None:
        self.x, self.y, self.z = self.z, self.y, -self.x

    def rotate_around_z(self) -> None:
        self.x, self.y, self.z = self.y, -self.x, self.z


class Scanner:
    position: Vector3

    def __init__(self, beacons: list[Vector3]) -> None:
        self.beacons = beacons
        self.distances = {a.distance_to(b) for a, b in combinations(beacons, 2)}

    def generate_all_rotations(self) -> None:
        """Generate all 24 beacon orientations.

        Beacons are sequentially rotated around the following axes:
            0) None     1) X       2) X        3) X
            4) XY       5) X       6) X        7) X
            8) XY       9) X      10) X       11) X
           12) XY      13) X      14) X       15) X
           16) XYZ     17) X      18) X       19) X
           20) XZZ     21) X      22) X       23) X
        """
        yield
        for i in range(1, 24):
            for beacon in self.beacons:
                beacon.rotate_around_x()
            if i == 4 or i == 8 or i == 12:
                for beacon in self.beacons:
                    beacon.rotate_around_y()
            if i == 16:
                for beacon in self.beacons:
                    beacon.rotate_around_y()
                    beacon.rotate_around_z()
            if i == 20:
                for beacon in self.beacons:
                    beacon.rotate_around_z()
                    beacon.rotate_around_z()
            yield


def load_data(path: Path) -> list[Scanner]:
    with open(path) as fd:
        data = fd.read().split("\n\n")
    scanners = []
    for scanner_report in data:
        beacons = []
        for line in scanner_report.splitlines()[1:]:
            coords = [int(x) for x in line.split(",")]
            beacons.append(Vector3(*coords))
        scanners.append(Scanner(beacons))
    return scanners


def find_alignment(scanner: Scanner, aligned_scanner: Scanner) -> Vector3:
    for _ in scanner.generate_all_rotations():
        for fixed_beacon, rotating_beacon in product(aligned_scanner.beacons[11:], scanner.beacons):
            translation = fixed_beacon - rotating_beacon
            matches_num = 0
            for beacon in scanner.beacons:
                if beacon + translation in aligned_scanner.beacons:
                    matches_num += 1
                if matches_num >= 12:
                    return translation
    raise InsufficientOverlapError


def align_scanners(scanners: list[Scanner]) -> list[Scanner]:
    initial_scanner, *remaining_scanners = scanners
    initial_scanner.position = Vector3(0, 0, 0)
    aligned_scanners = [initial_scanner]
    while remaining_scanners:
        for current_scanner, aligned_scanner in product(remaining_scanners, aligned_scanners):
            if len(current_scanner.distances.intersection(aligned_scanner.distances)) >= 66:
                try:
                    translation = find_alignment(current_scanner, aligned_scanner)
                except InsufficientOverlapError:
                    continue
                else:
                    break
        current_scanner.position = translation
        for beacon in current_scanner.beacons:
            beacon.translate(translation)
        aligned_scanners.append(current_scanner)
        remaining_scanners.remove(current_scanner)
    return aligned_scanners


def part_one(data: list[Scanner]) -> int:
    aligned_scanners = align_scanners(data)
    unique_beacons = {beacon for scanner in aligned_scanners for beacon in scanner.beacons}
    return len(unique_beacons)


def part_two(data: list[Scanner]) -> int:
    max_distance = 0
    for scanner, other_scanner in combinations(data, 2):
        max_distance = max(max_distance, scanner.position.distance_to(other_scanner.position))
    return max_distance


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/19"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 79
    assert part_two(samples) == 3621

    print(part_one(data))
    print(part_two(data))
