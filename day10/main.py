"""Day 10 - Advent of Code"""
from __future__ import annotations

import os
from typing import List, Optional, Tuple

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


def parse(line: str) -> Tuple[List[str], Optional[str]]:
    stack = []

    for c in line:
        if c in ("(", "[", "{", "<"):
            stack.append(c)
        elif c in (")", "]", "}", ">"):
            opening_c = stack.pop(-1)

            if not matches(opening_c, c):
                return stack, c

    # Could be either valid expression or incomplete
    return stack, None


def solve_part_one(data: Data) -> int:
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137, None: 0}

    total_syntax_error_score = 0

    for line in data:
        _, illegal_character = parse(line)
        total_syntax_error_score += scores[illegal_character]

    return total_syntax_error_score


def autocomplete(stack: List[str]) -> List[str]:
    complementary_characters = {"(": ")", "[": "]", "{": "}", "<": ">"}

    return [complementary_characters[c] for c in stack[::-1]]


def compute_autocomplete_score(missing_characters: List[str]) -> int:
    scores = {")": 1, "]": 2, "}": 3, ">": 4}

    total_score = 0

    for c in missing_characters:
        total_score = total_score * 5 + scores[c]

    return total_score


def solve_part_two(data: Data) -> int:
    autocomplete_scores = []

    for line in data:
        stack, illegal_character = parse(line)

        if illegal_character is not None:
            continue

        if len(stack) > 0:  # Incomplete
            missing_characters = autocomplete(stack)
            autocomplete_scores.append(
                compute_autocomplete_score(missing_characters)
            )

    mid_index = len(autocomplete_scores) // 2
    final_score = sorted(autocomplete_scores)[mid_index]
    return final_score


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 26_397
            assert solve_part_two(data) == 288_957

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
