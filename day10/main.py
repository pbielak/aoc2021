"""Day 10 - Advent of Code"""
from __future__ import annotations

import os
from typing import List, Optional

Data = List[str]


def read_data(filename: str) -> Data:
    data = []
    with open(filename, "r") as fin:
        for line in fin.readlines():
            data.append(line.strip())

        return data


def matches(opening_character: str, closing_character: str) -> bool:
    allowed_pairs = {("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")}

    return (opening_character, closing_character) in allowed_pairs


def find_first_illegal_character(line: str) -> Optional[str]:
    stack = []

    for c in line:
        if c in ("(", "[", "{", "<"):
            stack.append(c)
        elif c in (")", "]", "}", ">"):
            opening_c = stack.pop(-1)

            if not matches(opening_c, c):
                return c

    return None


def solve_part_one(data: Data) -> int:
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137, None: 0}

    total_syntax_error_score = 0

    for line in data:
        illegal_character = find_first_illegal_character(line)
        total_syntax_error_score += scores[illegal_character]

    return total_syntax_error_score


def solve_part_two(data: Data) -> int:
    pass


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 26_397
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
