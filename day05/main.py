"""Day 5 - Advent of Code"""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
import os
from typing import Dict, Generator, List, Tuple

Point2D = Tuple[int, int]


class Line(ABC):

    @staticmethod
    def from_string(line: str) -> Line:
        start, end = line.split(" -> ")

        x1, y1 = start.split(",")
        x2, y2 = end.split(",")

        if y1 == y2:
            return HorizontalLine(x1=int(x1), x2=int(x2), y=int(y1))
        elif x1 == x2:
            return VerticalLine(x=int(x1), y1=int(y1), y2=int(y2))
        else:
            return DiagonalLine(x1=int(x1), y1=int(y1), x2=int(x2), y2=int(y2))

    @abstractmethod
    def get_points(self) -> Generator[Point2D, None, None]:
        pass


def custom_range(start: int, end: int) -> List[int]:
    """Handles cases where `start` > `end`."""
    if start < end:
        return list(range(start, end + 1))
    else:
        return list(reversed(range(end, start + 1)))


class HorizontalLine(Line):

    def __init__(self, x1: int, x2: int, y: int):
        self.x1 = x1
        self.x2 = x2
        self.y = y

    def get_points(self) -> Generator[Point2D, None, None]:
        for x in custom_range(self.x1, self.x2):
            yield x, self.y


class VerticalLine(Line):

    def __init__(self, x: int, y1: int, y2: int):
        self.x = x
        self.y1 = y1
        self.y2 = y2

    def get_points(self) -> Generator[Point2D, None, None]:
        for y in custom_range(self.y1, self.y2):
            yield self.x, y


class DiagonalLine(Line):

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_points(self) -> Generator[Point2D, None, None]:
        xs = custom_range(self.x1, self.x2)
        ys = custom_range(self.y1, self.y2)

        for x, y in zip(xs, ys):
            yield x, y


Data = List[Line]


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        return [
            Line.from_string(line.strip())
            for line in fin.readlines()
        ]


def get_point_count_grid(data: List[Line]) -> Dict[Point2D, int]:
    num_lines_at_point = defaultdict(int)

    for line in data:
        for x, y in line.get_points():
            num_lines_at_point[(x, y)] += 1

    return num_lines_at_point


def num_points_where_at_least_two_lines(data: List[Line]) -> int:
    num_lines_at_point = get_point_count_grid(data)

    solution = 0
    for num_lines in num_lines_at_point.values():
        if num_lines >= 2:
            solution += 1

    return solution


def solve_part_one(data: Data) -> int:
    return num_points_where_at_least_two_lines([
        line for line in data
        if isinstance(line, (HorizontalLine, VerticalLine))
    ])


def solve_part_two(data: Data) -> int:
    return num_points_where_at_least_two_lines(data)


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
