"""Day 3 - Advent of Code"""
import os
from typing import List, Tuple

Data = List[Tuple[int]]


def read_data(filename: str) -> Data:
    numbers = []
    with open(filename, "r") as fin:
        for line in fin.readlines():
            numbers.append(tuple(int(d) for d in line.strip()))

    return numbers


def find_most_common_bits(data: Data) -> List[int]:
    num_digits = len(data[0])
    num_diagnostic_entries = len(data)

    one_counts = [0] * num_digits

    for number in data:
        for idx in range(num_digits):
            # We can add `0` as it won't change the counter
            one_counts[idx] += number[idx]

    most_common_bits = [
        1 if one_counts[idx] >= num_diagnostic_entries / 2 else 0
        for idx in range(num_digits)
    ]

    return most_common_bits


def solve_part_one(data: Data) -> int:
    """Solution for part 1.

    The `gamma rate` is a binary number where each bit is the most common bit
    among the diagnostic report, whereas the `epsilon rate` is built using the
    least common bit. In binary numbers there are just two options for each bit
    value: `0` and `1`. So it is enough to find the gamma rate and then compute
    the epsilon rate as the negation of the gamma rate (if the most common bit
    at any position is `1`, the least common bit will be `0`, and vice versa).
    """
    num_digits = len(data[0])

    most_common_bits = find_most_common_bits(data)

    gamma_rate = int("".join([str(b) for b in most_common_bits]), base=2)
    epsilon_rate = ~gamma_rate & (2**num_digits - 1)

    return gamma_rate * epsilon_rate


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Part 1
        solution_one = solve_part_one(data)

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
        )


if __name__ == "__main__":
    main()
