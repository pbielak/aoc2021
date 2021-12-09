"""Day 9 - Advent of Code"""
from __future__ import annotations

import os
from typing import List, Tuple

Data = Tuple[Tuple[int]]


def read_data(filename: str) -> Data:
    data = []
    with open(filename, "r") as fin:
        for line in fin.readlines():
            data.append(tuple(int(height) for height in line.strip()))

        return tuple(data)


def get_adjacent_indices(
    x: int,
    y: int,
    width: int,
    height: int,
) -> List[Tuple[int, int]]:
    indices = []

    if x > 0:
        indices.append((x - 1, y))  # Left

    if x < width - 1:
        indices.append((x + 1, y))  # Right

    if y > 0:
        indices.append((x, y - 1))  # Up

    if y < height - 1:
        indices.append((x, y + 1))  # Down

    return indices


def solve_part_one(data: Data) -> int:
    total_risk_level = 0

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            neighbor_indices = get_adjacent_indices(
                x=j,
                y=i,
                width=len(row),
                height=len(data),
            )
            if all(value < data[y][x] for x, y in neighbor_indices):
                risk = value + 1
                total_risk_level += risk

    return total_risk_level


def solve_part_two(data: Data) -> int:
    pass


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 15
            assert solve_part_two(data) == None

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
