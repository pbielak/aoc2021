"""Day 16 - Advent of Code"""
from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from functools import reduce
import os
from typing import List, Tuple


Data = str

HEX_2_BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        return fin.readline().strip()


def hex2bin(hex_value: str) -> str:
    bin_value = ""

    for hc in hex_value:
        bin_value += HEX_2_BIN[hc]

    return bin_value


def parse(bin_packet: str) -> Packet:
    return parse_packet(bin_packet)[0]


def contains_packet(payload: str) -> bool:
    return len(payload) > 0 and payload.count("1") > 0


def parse_packet(bin_packet: str) -> Tuple[Packet, str]:
    # Parse header
    version, type_id = parse_header(bin_packet)
    payload = bin_packet[6:]

    if type_id == 4:
        packet, remaining_payload = LiteralPacket.from_binary(
            version, type_id, payload,
        )
    else:
        packet, remaining_payload = OperatorPacket.from_binary(
            version, type_id, payload
        )

    return packet, remaining_payload


def parse_header(raw_packet: str) -> Tuple[int, int]:
    version = int(raw_packet[:3], 2)
    type_id = int(raw_packet[3:6], 2)

    return version, type_id


@dataclass
class Packet:
    version: int
    type_id: int

    @abstractmethod
    def evaluate(self) -> int:
        pass


@dataclass
class LiteralPacket(Packet):
    value: int

    def evaluate(self) -> int:
        return self.value

    @staticmethod
    def from_binary(version: int, type_id: int, payload: str):
        value = ""

        while len(payload) > 0:
            group, payload = payload[:5], payload[5:]

            value += group[1:]

            if group[0] == "0":  # Last packet
                break

        value = int(value, 2)

        packet = LiteralPacket(version=version, type_id=type_id, value=value)
        remaining_payload = payload

        return packet, remaining_payload


@dataclass
class OperatorPacket(Packet):
    nested_packets: List[Packet]

    def evaluate(self) -> int:
        values = [p.evaluate() for p in self.nested_packets]

        if self.type_id == 0:  # Sum
            return sum(values)
        elif self.type_id == 1:  # Product
            return reduce(lambda x, y: x * y, values)
        elif self.type_id == 2:  # Minimum
            return min(values)
        elif self.type_id == 3:  # Maximum
            return max(values)
        elif self.type_id == 5:  # Greater
            assert len(values) == 2
            return int(values[0] > values[1])
        elif self.type_id == 6:  # Less
            assert len(values) == 2
            return int(values[0] < values[1])
        elif self.type_id == 7:  # Equal
            assert len(values) == 2
            return int(values[0] == values[1])
        else:
            raise ValueError(f"Unknown packet type: {self.type_id}")

    @staticmethod
    def from_binary(version: int, type_id: int, payload: str):
        length_type_id = payload[0]

        if length_type_id == "0":
            total_length = int(payload[1:16], 2)
            nested_packets_raw = payload[16:]

            nested_packets = []
            used_bits = 0

            while used_bits != total_length:
                np, remaining = parse_packet(nested_packets_raw)

                nested_packets.append(np)
                used_bits += len(nested_packets_raw) - len(remaining)
                nested_packets_raw = remaining
        else:
            total_num_nested_packets = int(payload[1:12], 2)
            nested_packets_raw = payload[12:]

            nested_packets = []
            while len(nested_packets) != total_num_nested_packets:
                np, nested_packets_raw = parse_packet(nested_packets_raw)

                nested_packets.append(np)

            assert len(nested_packets) == total_num_nested_packets

        packet = OperatorPacket(
            version=version,
            type_id=type_id,
            nested_packets=nested_packets,
        )
        remaining_payload = nested_packets_raw

        return packet, remaining_payload


def sum_of_version_numbers(packet: Packet) -> int:
    if isinstance(packet, LiteralPacket):
        return packet.version

    return sum([
        sum_of_version_numbers(nested_packet)
        for nested_packet in packet.nested_packets
    ]) + packet.version


def solve_part_one(data: Data) -> int:
    packet = parse(hex2bin(data))
    assert isinstance(packet, (LiteralPacket, OperatorPacket))

    return sum_of_version_numbers(packet)


def solve_part_two(data: Data) -> int:
    packet = parse(hex2bin(data))
    assert isinstance(packet, OperatorPacket)

    return packet.evaluate()


def run_tests():
    # Case 1
    out_1 = parse(hex2bin("D2FE28"))
    assert isinstance(out_1, LiteralPacket)
    assert out_1.value == 2021

    # Case 2
    out_2 = parse(hex2bin("38006F45291200"))
    assert isinstance(out_2, OperatorPacket)
    assert len(out_2.nested_packets) == 2
    assert isinstance(out_2.nested_packets[0], LiteralPacket)
    assert out_2.nested_packets[0].value == 10
    assert isinstance(out_2.nested_packets[1], LiteralPacket)
    assert out_2.nested_packets[1].value == 20

    # Case 3
    out_3 = parse(hex2bin("EE00D40C823060"))
    assert isinstance(out_3, OperatorPacket)
    assert len(out_3.nested_packets) == 3
    assert isinstance(out_3.nested_packets[0], LiteralPacket)
    assert out_3.nested_packets[0].value == 1
    assert isinstance(out_3.nested_packets[1], LiteralPacket)
    assert out_3.nested_packets[1].value == 2
    assert isinstance(out_3.nested_packets[2], LiteralPacket)
    assert out_3.nested_packets[2].value == 3

    # Sum of version numbers
    assert solve_part_one("8A004A801A8002F478") == 16
    assert solve_part_one("620080001611562C8802118E34") == 12
    assert solve_part_one("C0015000016115A2E0802F182340") == 23
    assert solve_part_one("A0016C880162017C3686B18A3D4780") == 31

    # Expression evaluation
    assert solve_part_two("C200B40A82") == 3
    assert solve_part_two("04005AC33890") == 54
    assert solve_part_two("880086C3E88112") == 7
    assert solve_part_two("CE00C43D881120") == 9
    assert solve_part_two("D8005AC2A8F0") == 1
    assert solve_part_two("F600BC2D8F") == 0
    assert solve_part_two("9C005AC2F8F0") == 0
    assert solve_part_two("9C0141080250320F1802104A08") == 1


def main():
    run_tests()

    files = ["input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Part 1
        solution_one = solve_part_one(data)

        # Part 2
        solution_two = solve_part_two(data)

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
