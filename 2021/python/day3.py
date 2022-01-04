# https://adventofcode.com/2021/day/3

from pathlib import Path


def load_data(path):
    with open(path) as fd:
        return fd.readlines()


def bin_to_int(binary):
    str_binary = "".join(str(bit) for bit in binary)
    return int(str_binary, 2)


def negate(bit):
    return int(not bit)


def most_common(bits):
    return 1 if sum(int(bit) for bit in bits) >= len(bits) / 2 else 0


def most_common_bits(numbers):
    return list(map(lambda column: most_common(column), zip(*numbers)))


def least_common_bits(numbers):
    return list(map(lambda column: negate(most_common(column)), zip(*numbers)))


def filter_numbers(numbers, criteria_gen):
    numbers = numbers.copy()
    position = 0
    while len(numbers) > 1:
        criteria = criteria_gen(numbers)[position]
        numbers = [number for number in numbers if int(number[position]) == criteria]
        position += 1
    return numbers[0]


def part_one(data):
    gamma_rate = bin_to_int(most_common_bits(data))
    eps_rate = bin_to_int(least_common_bits(data))
    return gamma_rate * eps_rate


def part_two(data):
    oxygen_gen_rating = bin_to_int(filter_numbers(data, most_common_bits))
    co2_scrubber_rating = bin_to_int(filter_numbers(data, least_common_bits))
    return oxygen_gen_rating * co2_scrubber_rating


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/03"
    samples = load_data(input_dir / "samples.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples) == 198
    assert part_two(samples) == 230

    print(part_one(data))
    print(part_two(data))
