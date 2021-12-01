"""Day 1 - Advent of Code"""
import os
from typing import List


def read_data(filename: str) -> List[int]:
    with open(filename, "r") as fin:
        values = [int(line) for line in fin.readlines()]
        return values


def solve_part_one(data: List[int]) -> int:
    num_increased = 0

    for idx in range(0, len(data) - 1):
        if data[idx + 1] > data[idx]:
            num_increased += 1

    return num_increased


def solve_part_two(data: List[int], window_size: int = 3) -> int:
    num_increased = 0

    for idx in range(0, len(data) - window_size):
        current_window_sum = sum(data[idx:idx + window_size])
        next_window_sum = sum(data[idx + 1:idx + 1 + window_size])

        if next_window_sum > current_window_sum:
            num_increased += 1

    return num_increased


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Part 1
        solution_one = solve_part_one(data)

        # Part 2
        solution_two = solve_part_two(data)

        # NOTE(pbielak): Part 1 can be also solved by calling `solve_part_two`
        assert solve_part_two(data, window_size=1) == solution_one

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
