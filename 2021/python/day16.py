# https://adventofcode.com/2021/day/16

from collections import namedtuple
from math import prod
from pathlib import Path

Packet = namedtuple("Packet", "version type_id value subpackets")


def load_data(path):
    with open(path) as fd:
        return hex2bin(fd.read().strip())


def hex2bin(hex_str):
    return bin(int(hex_str, base=16))[2:].zfill(len(hex_str) * 4)


def get_literal_value(transmission, index):
    last_group = False
    bits = ""
    while not last_group:
        last_group = transmission[index] == "0"
        bits += transmission[index + 1 : index + 5]
        index += 5
    return int(bits, base=2), index


def get_subpackets_by_length(transmission, index):
    subpackets_len = int(transmission[index : index + 15], base=2)
    index += 15
    subpackets_end = index + subpackets_len
    subpackets = []
    while index < subpackets_end:
        packet, index = decode(transmission, index)
        subpackets.append(packet)
    return subpackets, index


def get_subpackets_by_number(transmission, index):
    subpackets_num = int(transmission[index : index + 11], base=2)
    index += 11
    subpackets = []
    for _ in range(subpackets_num):
        packet, index = decode(transmission, index)
        subpackets.append(packet)
    return subpackets, index


def calculate_value(type_id, subpackets):
    match type_id:
        case 0:
            value = sum([packet.value for packet in subpackets])
        case 1:
            value = prod([packet.value for packet in subpackets])
        case 2:
            value = min([packet.value for packet in subpackets])
        case 3:
            value = max([packet.value for packet in subpackets])
        case 5:
            value = int(subpackets[0].value > subpackets[1].value)
        case 6:
            value = int(subpackets[0].value < subpackets[1].value)
        case 7:
            value = int(subpackets[0].value == subpackets[1].value)
        case _:
            raise RuntimeError("Unsupported type ID")
    return value


def decode(transmission, index):
    version = int(transmission[index : index + 3], base=2)
    type_id = int(transmission[index + 3 : index + 6], base=2)
    index += 6
    if type_id == 4:
        value, index = get_literal_value(transmission, index)
        return Packet(version, type_id, value, []), index
    else:
        length_type_id = transmission[index]
        index += 1
        if length_type_id == "0":
            subpackets, index = get_subpackets_by_length(transmission, index)
        else:
            subpackets, index = get_subpackets_by_number(transmission, index)
        return (
            Packet(version, type_id, calculate_value(type_id, subpackets), subpackets),
            index,
        )


def sum_versions(packet):
    return packet.version + sum([sum_versions(packet) for packet in packet.subpackets])


def part_one(data):
    packet, _ = decode(data, index=0)
    return sum_versions(packet)


def part_two(data):
    packet, _ = decode(data, index=0)
    return packet.value


if __name__ == "__main__":
    input_dir = Path().resolve().parent / "inputs/16"
    samples1 = load_data(input_dir / "samples1.in")
    samples2 = load_data(input_dir / "samples2.in")
    samples3 = load_data(input_dir / "samples3.in")
    samples4 = load_data(input_dir / "samples4.in")
    samples5 = load_data(input_dir / "samples5.in")
    samples6 = load_data(input_dir / "samples6.in")
    samples7 = load_data(input_dir / "samples7.in")
    samples8 = load_data(input_dir / "samples8.in")
    samples9 = load_data(input_dir / "samples9.in")
    samples10 = load_data(input_dir / "samples10.in")
    samples11 = load_data(input_dir / "samples11.in")
    samples12 = load_data(input_dir / "samples12.in")
    data = load_data(input_dir / "data.in")

    assert part_one(samples1) == 16
    assert part_one(samples2) == 12
    assert part_one(samples3) == 23
    assert part_one(samples4) == 31
    assert part_two(samples5) == 3
    assert part_two(samples6) == 54
    assert part_two(samples7) == 7
    assert part_two(samples8) == 9
    assert part_two(samples9) == 1
    assert part_two(samples10) == 0
    assert part_two(samples11) == 0
    assert part_two(samples12) == 1

    print(part_one(data))
    print(part_two(data))
