"""Day 19 - Advent of Code"""
from __future__ import annotations

import os
from typing import Generator, List, Tuple


Point = Tuple[int, int, int]
Data = List[List[Point]]


def read_data(filename: str) -> Data:
    data = []
    with open(filename, "r") as fin:
        for report in fin.read().split("\n\n"):
            coordinates = [
                tuple(int(pos) for pos in line.split(","))
                for line in report.split("\n")[1:]
            ]

            data.append(coordinates)

        return data


def get_transformed(
    points: List[Point],
) -> Generator[Tuple[str, List[Point]], None, None]:
    """Matrices found at: `http://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm`"""
    matrices = [
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
        [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
        [[1, 0, 0], [0, 0, 1], [0, -1, 0]],

        [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
        [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
        [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
        [[0, 0, -1], [1, 0, 0], [0, -1, 0]],

        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
        [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
        [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],

        [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
        [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
        [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],
        [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],

        [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
        [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
        [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
        [[0, -1, 0], [0, 0, -1], [1, 0, 0]],

        [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
        [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],
        [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
        [[0, 1, 0], [0, 0, -1], [-1, 0, 0]]
    ]
    assert len(matrices) == 24

    def mm(M, v):
        return [
            M[0][0] * v[0] + M[0][1] * v[1] + M[0][2] * v[2],
            M[1][0] * v[0] + M[1][1] * v[1] + M[1][2] * v[2],
            M[2][0] * v[0] + M[2][1] * v[1] + M[2][2] * v[2],
        ]

    for matrix in matrices:
        yield "", [mm(matrix, p) for p in points]


def translate(T: Point, points: List[Point]) -> List[Point]:
    return [(p[0] + T[0], p[1] + T[1], p[2] + T[2]) for p in points]


def align(
    scanner_a: List[Point],
    scanner_b: List[Point],
) -> Tuple[Point, List[Point]]:
    for transform_name, transformed in get_transformed(scanner_b):
        for i, a in enumerate(scanner_a):
            for j, b in enumerate(transformed):
                T = (a[0] - b[0], a[1] - b[1], a[2] - b[2])
                translated = translate(T, transformed)

                num_shared = len(set(translated).intersection(set(scanner_a)))

                if num_shared >= 12:
                    combined_points = list(
                        set(scanner_a).union(set(translated))
                    )

                    return T, combined_points


def find_largest_manhattan_distance(scanner_positions: List[Point]) -> int:
    largest_distance = 0
    for pos1 in scanner_positions:
        for pos2 in scanner_positions:
            md = (
                abs(pos1[0] - pos2[0])
                + abs(pos1[1] - pos2[1])
                + abs(pos1[2] - pos2[2])
            )

            largest_distance = max(largest_distance, md)

    return largest_distance


def solve(data: Data) -> Tuple[int, int]:
    all_beacons = data[0]
    scanner_positions = [None] * len(data)
    scanner_positions[0] = (0, 0, 0)
    merged = {0}

    while len(merged) != len(data):
        for i in range(1, len(data)):
            if i in merged:
                continue

            result = align(all_beacons, data[i])

            if result is None:
                continue

            scanner_pos, all_beacons = result
            scanner_positions[i] = scanner_pos
            merged.add(i)

            print(
                f"Aligned scanner: {i} || "
                f"Completed: {len(merged)} / {len(data)}"
            )

    part1 = len(all_beacons)
    part2 = find_largest_manhattan_distance(scanner_positions)
    return part1, part2


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            ex1, ex2 = solve(data)
            assert ex1 == 79
            assert ex2 == 3_621

        solution_one, solution_two = solve(data)

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
