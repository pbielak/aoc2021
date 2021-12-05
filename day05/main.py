"""Day 5 - Advent of Code"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import os
from typing import Generator, List, Tuple


@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int

    def get_points(self) -> Generator[Tuple[int, int], None, None]:
        x1, x2 = self.x1, self.x2

        if x1 > x2:
            x1, x2 = x2, x1

        y1, y2 = self.y1, self.y2

        if y1 > y2:
            y1, y2 = y2, y1

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                yield x, y


Data = List[Line]


def read_data(filename: str) -> Data:
    data = []
    with open(filename, "r") as fin:
        for line in fin.readlines():
            start, end = line.strip().split(" -> ")

            x1, y1 = start.split(",")
            x2, y2 = end.split(",")

            data.append(Line(x1=int(x1), y1=int(y1), x2=int(x2), y2=int(y2)))

    return data


def solve_part_one(data: Data) -> int:
    num_lines_at_point = defaultdict(int)

    for line in data:
        # Consider only horizontal and vertical lines
        if (line.x1 == line.x2) or (line.y1 == line.y2):
            for x, y in line.get_points():
                num_lines_at_point[(x, y)] += 1
    solution = 0

    for num_lines in num_lines_at_point.values():
        if num_lines >= 2:
            solution += 1

    return solution


def solve_part_two(data: Data) -> int:
    pass


def main():
    files = ["example.txt", "input.txt"]

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
