"""Day 11 - Advent of Code"""
from __future__ import annotations

from copy import deepcopy
import os
from typing import List, Optional, Tuple

Data = List[List[int]]
Position = Tuple[int, int]


def read_data(filename: str) -> Data:
    data = []
    with open(filename, "r") as fin:
        for line in fin.readlines():
            data.append([int(energy_level) for energy_level in line.strip()])

        return data


def get_neighbors(row: int, col: int, grid_size: int) -> List[Position]:
    neighbor_positions = []

    has_space_on_left = col > 0
    has_space_on_right = col < grid_size - 1
    has_space_above = row > 0
    has_space_below = row < grid_size - 1

    # Left
    if has_space_on_left:
        neighbor_positions.append((row, col - 1))

    # Right
    if has_space_on_right:
        neighbor_positions.append((row, col + 1))

    # Up
    if has_space_above:
        neighbor_positions.append((row - 1, col))

        if has_space_on_left:
            neighbor_positions.append((row - 1, col - 1))

        if has_space_on_right:
            neighbor_positions.append((row - 1, col + 1))

    # Down
    if has_space_below:
        neighbor_positions.append((row + 1, col))

        if has_space_on_left:
            neighbor_positions.append((row + 1, col - 1))

        if has_space_on_right:
            neighbor_positions.append((row + 1, col + 1))

    return neighbor_positions


def simulate_single_step(
    energy_levels: Data,
    grid_size: int = 10,
) -> Tuple[Data, int]:
    energy_levels = deepcopy(energy_levels)

    # Increase energy levels
    for row in range(grid_size):
        for col in range(grid_size):
            energy_levels[row][col] += 1

    has_flashed = set()

    while True:
        flash_indices = []

        for row in range(grid_size):
            for col in range(grid_size):
                if energy_levels[row][col] > 9:
                    flash_indices.append((row, col))

        if len(flash_indices) == 0:
            break

        for row, col in flash_indices:
            # Flash
            energy_levels[row][col] = 0
            has_flashed.add((row, col))

            # Increase neighbor energy levels
            for nrow, ncol in get_neighbors(row, col, grid_size=grid_size):
                if (nrow, ncol) not in has_flashed:
                    energy_levels[nrow][ncol] += 1

    return energy_levels, len(has_flashed)


def solve_part_one(data: Data) -> int:
    total_flashes = 0

    for _ in range(100):
        data, num_flashes = simulate_single_step(data)
        total_flashes += num_flashes

    return total_flashes


def solve_part_two(data: Data) -> int:
    pass


def run_tests():
    assert simulate_single_step(energy_levels=[
        [1, 1, 1, 1, 1],
        [1, 9, 9, 9, 1],
        [1, 9, 1, 9, 1],
        [1, 9, 9, 9, 1],
        [1, 1, 1, 1, 1],
    ], grid_size=5) == (
        [
            [3, 4, 5, 4, 3],
            [4, 0, 0, 0, 4],
            [5, 0, 0, 0, 5],
            [4, 0, 0, 0, 4],
            [3, 4, 5, 4, 3],
        ],
        9
    )
    print("Mini-example test passed...")


def main():
    run_tests()

    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 1_656
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
