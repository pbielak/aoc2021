"""Day 9 - Advent of Code"""
from __future__ import annotations

from collections import defaultdict
import os
from typing import List, Tuple

Data = Tuple[Tuple[int]]
Position = Tuple[int, int]


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
) -> List[Position]:
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


def find_low_points(data: Data) -> List[Position]:
    low_points = []
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            neighbor_indices = get_adjacent_indices(
                x=j,
                y=i,
                width=len(row),
                height=len(data),
            )
            if all(value < data[y][x] for x, y in neighbor_indices):
                low_points.append((i, j))

    return low_points


def solve_part_one(data: Data) -> int:
    total_risk_level = 0

    for i, j in find_low_points(data):
        risk = data[i][j] + 1
        total_risk_level += risk

    return total_risk_level


def get_basin(low_point: Position, data: Data) -> List[Position]:
    visited = defaultdict(bool)
    queue = [low_point]

    while queue:
        i, j = queue.pop(0)
        visited[(i, j)] = True

        indices = get_adjacent_indices(
            x=j, y=i, width=len(data[0]), height=len(data),
        )

        for x, y in indices:
            if data[y][x] == 9:
                continue

            if visited[(y, x)]:
                continue

            queue.append((y, x))

    basin_indices = list(visited.keys())
    return basin_indices


def solve_part_two(data: Data) -> int:
    basin_sizes = []
    for low_point in find_low_points(data):
        basin_indices = get_basin(low_point, data)
        basin_sizes.append(len(basin_indices))

    basin_sizes = sorted(basin_sizes)

    return basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 15
            assert solve_part_two(data) == 1134

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
