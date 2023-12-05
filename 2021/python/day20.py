# https://adventofcode.com/2021/day/20

from itertools import product
from pathlib import Path

from pprint import pprint

OFFSETS = list(product([1, 0, -1], repeat=2))


def load_data(path: Path) -> tuple[list[int], list[list[int]]]:
    with open(path) as fd:
        algorithm, image = fd.read().split("\n\n")
    algorithm = [int(char == "#") for char in algorithm]
    image = [[int(char == "#") for char in row] for row in image.splitlines()]
    return algorithm, image


def pad(image: list[list[int]], value: int) -> list[list[int]]:
    padded_image = [[value, *row, value] for row in image]
    padded_image = [
        [value] * len(padded_image[0]),
        *padded_image,
        [value] * len(padded_image[0]),
    ]
    return padded_image


def enhance_image(image: list[list[int]], algorithm: list[int], repeat: int = 1) -> list[list[int]]:
    padding_value = 0
    for _ in range(repeat):
        padded_image = pad(image, padding_value)
        enhanced_image = [[0] * len(padded_image[0]) for _ in range(len(padded_image))]
        rows_num = len(enhanced_image)
        row_size = len(enhanced_image[0])
        for y in range(rows_num):
            for x in range(row_size):
                index = 0
                for bit_position, (dy, dx) in enumerate(OFFSETS):
                    pixel_x = x + dx
                    pixel_y = y + dy
                    if 0 <= pixel_x < row_size and 0 <= pixel_y < rows_num:
                        pixel = padded_image[pixel_y][pixel_x]
                    else:
                        pixel = padding_value
                    index += pixel * 2**bit_position
                enhanced_image[y][x] = algorithm[index]
        if padding_value == 0:
            padding_value = algorithm[0]
        else:
            padding_value = algorithm[-1]
        image = enhanced_image
    return image


def count_lit_pixels(image: list[list[int]]) -> int:
    return sum(sum(row) for row in image)


def part_one(data: tuple[list[int], list[list[int]]]) -> int:
    algorithm, image = data
    enhanced_image = enhance_image(image, algorithm, repeat=2)
    return count_lit_pixels(enhanced_image)


def part_two(data: tuple[list[int], list[list[int]]]) -> int:
    algorithm, image = data
    enhanced_image = enhance_image(image, algorithm, repeat=50)
    return count_lit_pixels(enhanced_image)


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/20"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 35
    assert part_two(samples) == 3351

    print(part_one(data))
    print(part_two(data))
