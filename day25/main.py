"""Day 25 - Advent of Code"""
from __future__ import annotations

from copy import deepcopy
import os
from typing import List, Tuple


class SeaFloor:

    def __init__(self, fields: List[List[str]]):
        self.fields = fields
        self.width = len(fields[0])
        self.height = len(fields)

    def copy(self) -> SeaFloor:
        return deepcopy(self)

    def __eq__(self, other: SeaFloor) -> bool:
        return all(
            sline == oline
            for sline, oline
            in zip(self.fields, other.fields)
        )

    def __getitem__(self, idx: Tuple[int, int]) -> str:
        row, col = idx

        return self.fields[row][col]

    def __setitem__(self, key: Tuple[int, int], value: str):
        row, col = key
        self.fields[row][col] = value

    def __repr__(self):
        return "\n".join("".join(line) for line in self.fields)


def read_data(filename: str) -> SeaFloor:
    with open(filename, "r") as fin:
        fields = [list(line.strip()) for line in fin.readlines()]
        return SeaFloor(fields)


def update(seafloor: SeaFloor) -> SeaFloor:
    out = seafloor.copy()

    east_facing_positions = [
        (row, col)
        for row in range(out.height)
        for col in range(out.width)
        if out[row, col] == ">"
    ]

    south_facing_positions = [
        (row, col)
        for row in range(out.height)
        for col in range(out.width)
        if out[row, col] == "v"
    ]

    # Update east facing ones
    east_updates = []
    for row, col in east_facing_positions:
        current_pos = row, col
        target_pos = row, (col + 1) % out.width

        if out[target_pos] == ".":
            east_updates.append((current_pos, target_pos))

    for cpos, tpos in east_updates:
        out[cpos] = "."
        out[tpos] = ">"

    # Update south facing ones
    south_updates = []
    for row, col in south_facing_positions:
        current_pos = row, col
        target_pos = (row + 1) % out.height, col

        if out[target_pos] == ".":
            south_updates.append((current_pos, target_pos))

    for cpos, tpos in south_updates:
        out[cpos] = "."
        out[tpos] = "v"

    return out


def solve_part_one(data: SeaFloor) -> int:
    step = 1

    prev = data

    while True:
        curr = update(seafloor=prev)

        if curr == prev:
            return step

        step += 1
        prev = curr


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Part 1
        solution_one = solve_part_one(data)

        # Test cases
        if filename == "example.txt":
            assert solution_one == 58

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
        )


if __name__ == "__main__":
    main()
