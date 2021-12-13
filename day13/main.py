"""Day 13 - Advent of Code"""
from __future__ import annotations

import os
from typing import List, NamedTuple, Tuple

DotPosition = Tuple[int, int]


class FoldInstruction:

    def __init__(self, axis: str, value: int):
        self._axis = axis
        self._value = value

    def apply(self, dots: List[DotPosition]) -> List[DotPosition]:
        out = []

        for x, y in dots:
            if self._axis == "x" and x > self._value:
                new_x = -(x - self._value) % self._value
            else:
                new_x = x

            if self._axis == "y" and y > self._value:
                new_y = -(y - self._value) % self._value
            else:
                new_y = y

            out.append((new_x, new_y))

        out = list(set(out))

        return out

    @staticmethod
    def from_str(instruction: str) -> FoldInstruction:
        axis, value = instruction.replace("fold along ", "").split("=")

        return FoldInstruction(axis, int(value))


class Data(NamedTuple):
    dots: List[DotPosition]
    fold_instructions: List[FoldInstruction]


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        dots, fold_instructions = fin.read().split("\n\n")

        dots = [
            tuple(int(pos) for pos in dot.split(","))
            for dot in dots.split("\n")
        ]

        fold_instructions = [
            FoldInstruction.from_str(instruction)
            for instruction in fold_instructions.split("\n")
        ]

        data = Data(dots=dots, fold_instructions=fold_instructions)

        return data


def solve_part_one(data: Data) -> int:
    first_instruction = data.fold_instructions[0]

    dots = first_instruction.apply(dots=data.dots)

    return len(dots)


def solve_part_two(data: Data) -> str:
    dots = data.dots

    for instruction in data.fold_instructions:
        dots = instruction.apply(dots)

    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)

    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y in dots:
        grid[y][x] = "#"

    return "\n".join(["".join(row) for row in grid])


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 17

        # Part 1
        solution_one = solve_part_one(data)

        # Part 2
        solution_two = solve_part_two(data)

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: \n{solution_two}\n"
        )


if __name__ == "__main__":
    main()
