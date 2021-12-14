"""Day 14 - Advent of Code"""
from __future__ import annotations

from collections import defaultdict
from math import ceil
import os
from typing import Dict, NamedTuple, Tuple


Atom = str
AtomPair = Tuple[Atom, Atom]
Polymer = Dict[AtomPair, int]


class Data(NamedTuple):
    start_polymer: Polymer
    insertion_rules: Dict[AtomPair, Atom]


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        polymer_str = fin.readline().strip()

        polymer = defaultdict(int)
        for atom_pair in zip(polymer_str, polymer_str[1:]):
            polymer[atom_pair] += 1

        fin.readline()

        insertion_rules = {}
        for line in fin.readlines():
            pattern, new_atom = line.strip().split(" -> ")
            insertion_rules[tuple(pattern)] = new_atom

        data = Data(start_polymer=polymer, insertion_rules=insertion_rules)
        return data


def perform_insertion(
    polymer: Polymer,
    insertion_rules: Dict[AtomPair, Atom],
) -> Polymer:
    out = defaultdict(int)

    for pair, count in polymer.items():
        assert pair in insertion_rules

        left, right = pair
        new_atom = insertion_rules[pair]

        out[(left, new_atom)] += count
        out[(new_atom, right)] += count

    return out


def compute_atom_counts(
    start_polymer: Polymer,
    insertion_rules: Dict[AtomPair, Atom],
    num_steps: int,
) -> Dict[str, int]:
    polymer = start_polymer.copy()

    for step in range(num_steps):
        polymer = perform_insertion(
            polymer=polymer,
            insertion_rules=insertion_rules,
        )

    atom_counts = defaultdict(int)

    for (left, right), count in polymer.items():
        atom_counts[left] += count
        atom_counts[right] += count

    for atom, count in atom_counts.items():
        atom_counts[atom] = ceil(count / 2)

    return atom_counts


def solve(data: Data, num_steps: int) -> int:
    atom_counts = compute_atom_counts(
        start_polymer=data.start_polymer,
        insertion_rules=data.insertion_rules,
        num_steps=num_steps,
    )

    most_common_atom = max(atom_counts.values())
    least_common_atom = min(atom_counts.values())

    return most_common_atom - least_common_atom


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve(data, num_steps=10) == 1_588
            assert solve(data, num_steps=40) == 2_188_189_693_529

        # Part 1
        solution_one = solve(data, num_steps=10)

        # Part 2
        solution_two = solve(data, num_steps=40)

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
