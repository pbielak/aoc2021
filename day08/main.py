"""Day 8 - Advent of Code"""
from __future__ import annotations

import os
from typing import Dict, List, NamedTuple, Tuple

DisplayOutput = Tuple[str]


class Entry(NamedTuple):
    observed: List[DisplayOutput]
    output: List[DisplayOutput]


Data = List[Entry]


def read_data(filename: str) -> Data:
    data = []
    with open(filename, "r") as fin:
        for line in fin.readlines():
            observed, output = line.strip().split(" | ")

            observed = [
                to_canonical_display_output(obs)
                for obs in observed.split(" ")
            ]

            output = [
                to_canonical_display_output(out)
                for out in output.split(" ")
            ]

            data.append(Entry(observed=observed, output=output))

        return data


def to_canonical_display_output(out: str) -> DisplayOutput:
    sorted_segments: List[str] = sorted(list(out))
    return tuple(sorted_segments)


def solve_part_one(data: Data) -> int:
    # We need to count how many times the digits 1, 4, 7, 8 occurred in the
    # outputs (i.e., after the "|" character). Those digits are composed of
    # 2, 4, 3 and 7 segments, respectively. So we need to count how many times
    # the output had a length of 2, 4, 3 or 7.
    total = 0

    for entry in data:
        for output in entry.output:
            if len(output) in (2, 4, 3, 7):
                total += 1

    return total


AVAILABLE_SEGMENTS = ("a", "b", "c", "d", "e", "f", "g")
SEGMENTS_TO_DIGIT = {
    ("a", "b", "c",      "e", "f", "g"): 0,
    (          "c",           "f",    ): 1,
    ("a",      "c", "d", "e",      "g"): 2,
    ("a",      "c", "d",      "f", "g"): 3,
    (     "b", "c", "d",      "f",    ): 4,
    ("a", "b",      "d",      "f", "g"): 5,
    ("a", "b",      "d", "e", "f", "g"): 6,
    ("a",      "c",           "f",    ): 7,
    ("a", "b", "c", "d", "e", "f", "g"): 8,
    ("a", "b", "c", "d",      "f", "g"): 9,
}


def build_mapping(observed: List[DisplayOutput]) -> Dict[str, str]:
    original_to_mixed = {
        segment.upper(): set()
        for segment in AVAILABLE_SEGMENTS
    }

    from collections import defaultdict
    observations_of_given_length = defaultdict(list)
    for observation in observed:
        observations_of_given_length[len(observation)].append(observation)

    # The observation of length 2 is representing digit "1". We know that this
    # digit uses segments "C" and "F", so we have two candidates for each one.
    assert len(observations_of_given_length[2]) == 1
    candidates_CF = set(observations_of_given_length[2][0])

    original_to_mixed["C"] = candidates_CF
    original_to_mixed["F"] = candidates_CF

    # The observation of length 3 is representing digit "7". It uses segments:
    # "A", "C" and "F". We already have some information about "C" and "F", so
    # we can easily deduce "A".
    assert len(observations_of_given_length[3]) == 1
    obs = observations_of_given_length[3][0]

    segment_A = set(obs).difference(original_to_mixed["C"])
    assert len(segment_A) == 1

    original_to_mixed["A"] = segment_A

    # The observation of length 4 is representing digit "4". It uses segments:
    # "B", "C", "D" and "F". We already have some information about "C" and "F".
    # Hence, we can update candidates for "B" and "D".
    assert len(observations_of_given_length[4]) == 1
    obs = observations_of_given_length[4][0]

    candidates_BD = set(obs).difference(original_to_mixed["C"])
    assert len(candidates_BD) == 2

    original_to_mixed["B"] = candidates_BD
    original_to_mixed["D"] = candidates_BD

    # There are three observations of length 5 and they represent the following
    # digits: "2", "3" and "5". We know that:
    # - digit "2" uses: "A",      "C", "D", "E",      "G"
    # - digit "3" uses: "A",      "C", "D",      "F", "G"
    # - digit "4" uses: "A", "B",      "D",      "F", "G"
    # We see that all three of them use segments: "A", "D" and "G".
    #
    # 1) We already know segment "A".
    # 2) Using the information from the previous step (gathering "B" and "D"),
    # we can easily determine which is B and which D (D will be in both sets).
    assert len(observations_of_given_length[5]) == 3
    obs = observations_of_given_length[5]

    intersection_ADG = set.intersection(set(obs[0]), set(obs[1]), set(obs[2]))
    intersection_DG = intersection_ADG.difference(segment_A)
    segment_D = intersection_DG.intersection(candidates_BD)
    segment_B = candidates_BD.difference(segment_D)
    segment_G = intersection_DG.difference(segment_D)

    original_to_mixed["B"] = segment_B
    original_to_mixed["D"] = segment_D
    original_to_mixed["G"] = segment_G

    # There are three observations of length 6 and they represent the followung
    # digits: "0", "6", "9". We know that:
    # - digit "0" uses: "A", "B", "C",    , "E", "F", "G"
    # - digit "6" uses: "A", "B",      "D", "E", "F", "G"
    # - digit "9" uses: "A", "B", "C", "D",      "F", "G"
    # We see that all three of them use segments "A", "B", "F" and "G".
    #
    # 1) We already know: "A", "B" and "G". Hence, we automatically know "F".
    # 2) We already determined candidates for "C" and "F". We know "F" from 1),
    # hence we know the exact value for "C".
    # 3) Segment "E" will be the only unused segment.
    assert len(observations_of_given_length[6]) == 3
    obs = observations_of_given_length[6]

    intersection_ABFG = set.intersection(set(obs[0]), set(obs[1]), set(obs[2]))

    segment_F = (
        intersection_ABFG
        .difference(segment_A)
        .difference(segment_B)
        .difference(segment_G)
    )

    original_to_mixed["F"] = segment_F

    segment_C = candidates_CF.difference(segment_F)
    segment_E = set(AVAILABLE_SEGMENTS).difference(set.union(
        segment_A, segment_B, segment_C, segment_D, segment_F, segment_G
    ))

    assert len(segment_C) == 1
    assert len(segment_E) == 1

    original_to_mixed["C"] = segment_C
    original_to_mixed["E"] = segment_E

    # Convert back to lowercase identifiers and reverse the mapping.
    mixed_to_original = {
        v.pop(): k.lower()
        for k, v in original_to_mixed.items()
    }
    return mixed_to_original


def output_to_digit(output: DisplayOutput, mapping: Dict[str, str]) -> int:
    original_segments = tuple(sorted([mapping[s] for s in output]))
    return SEGMENTS_TO_DIGIT[original_segments]


def solve_part_two(data: Data) -> int:
    total = 0

    for entry in data:
        mapping = build_mapping(observed=entry.observed)

        output_digits = [
            str(output_to_digit(output=out, mapping=mapping))
            for out in entry.output
        ]
        number = int("".join(output_digits))

        total += number

    return total


def main():
    files = ["example-mini.txt", "example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example-mini.txt":
            assert solve_part_one(data) == 0
            assert solve_part_two(data) == 5353

        if filename == "example.txt":
            assert solve_part_one(data) == 26
            assert solve_part_two(data) == 61229

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
