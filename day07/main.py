"""Day 7 - Advent of Code"""
from __future__ import annotations

import os
from statistics import median
from typing import List

Data = List[int]


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        return [int(position) for position in fin.readline().split(",")]


def compute_fuel_cost(positions: Data, target_position: int) -> int:
    return sum([abs(p - target_position) for p in positions])


def solve_part_one_naive(data: Data) -> int:
    return min([
        compute_fuel_cost(positions=data, target_position=target_position)
        for target_position in range(min(data), max(data) + 1)
    ])


def solve_part_one_using_median(data: Data) -> int:
    target_position = int(median(data))
    return compute_fuel_cost(positions=data, target_position=target_position)


def compute_new_fuel_cost(positions: Data, target_position: int) -> int:
    # Previously the cost of moving a submarine from its current point `p` to
    # the target position `t` was equal to `|p - t|`. Right now each step takes
    # one more than the previous one, which is a simple arithmetic series, to be
    # precise it's the sum of the first k natural numbers: `1 + 2 + ... + k`,
    # where `k = |p - t|`. This has a closed-form solution: `\frac{k(k+1)}{2}`,
    # which expands to: `\frac{|p - t| (|p - t| + 1)}{2}`.
    def single_submarine_cost(p: int) -> int:
        k = abs(p - target_position)
        return (k * (k + 1)) // 2

    return sum([single_submarine_cost(p) for p in positions])


def solve_part_two(data: Data) -> int:
    return min([
        compute_new_fuel_cost(positions=data, target_position=target_position)
        for target_position in range(min(data), max(data) + 1)
    ])


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one_naive(data) == 37
            assert solve_part_one_using_median(data) == 37
            assert solve_part_two(data) == 168

        # Part 1
        solution_one = solve_part_one_using_median(data)

        # Part 2
        solution_two = solve_part_two(data)

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
