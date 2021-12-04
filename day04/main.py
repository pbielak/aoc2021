"""Day 4 - Advent of Code"""
from __future__ import annotations

import os
from typing import List, NamedTuple


class Data(NamedTuple):
    numbers: List[int]
    boards: List[Board]


class Board:
    SIZE = 5

    def __init__(self, values: List[List[int]]):
        self._values = values
        self._is_marked: List[List[bool]] = [
            [False for _ in range(self.SIZE)]
            for _ in range(self.SIZE)
        ]

    def mark(self, number: int):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self._values[i][j] == number:
                    self._is_marked[i][j] = True

    def has_won(self) -> bool:
        # Check rows
        for i in range(self.SIZE):
            if all(marked for marked in self._is_marked[i]):
                return True

        # Check columns
        for j in range(self.SIZE):
            if all(self._is_marked[i][j] for i in range(self.SIZE)):
                return True

        return False

    def sum_of_unmarked(self) -> int:
        total = 0
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if not self._is_marked[i][j]:
                    total += self._values[i][j]

        return total


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        numbers = [int(n) for n in fin.readline().strip().split(",")]
        boards = []

        while fin.readline():  # Read empty line before board
            values = []
            for _ in range(Board.SIZE):
                line = (
                    fin.readline()
                    .strip()
                    .replace("  ", " ")
                )
                values.append([int(n) for n in line.split(" ")])

            boards.append(Board(values=values))

    data = Data(numbers=numbers, boards=boards)
    return data


def solve_part_one(data: Data) -> int:
    for n in data.numbers:
        for board in data.boards:
            board.mark(number=n)

            if board.has_won():
                return board.sum_of_unmarked() * n


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
