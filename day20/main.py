"""Day 20 - Advent of Code"""
from __future__ import annotations

import os
from typing import List, NamedTuple, Tuple

Image = List[str]


class Data(NamedTuple):
    enhancement_lookup: str
    image: Image


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        enhancement_lookup, image = fin.read().split("\n\n")
        image = image.split("\n")

        return Data(enhancement_lookup=enhancement_lookup, image=image)


def add_background(image: Image, background: str, delta: int = 3) -> Image:
    width = len(image[0])

    enlarged = []

    for _ in range(delta):
        enlarged.append(background * (width + 2 * delta))

    for line in image:
        enlarged.append((background * delta) + line + (background * delta))

    for _ in range(delta):
        enlarged.append(background * (width + 2 * delta))

    return enlarged


def get_neighbor_indices(row: int, col: int) -> List[Tuple[int, int]]:
    return [
        # Top row
        (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
        # Middle row
        (row, col - 1), (row, col), (row, col + 1),
        # Bottom row
        (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
    ]


def enhance_image(image: Image, enhancement_lookup: str) -> List[str]:
    enhanced = []
    for row in range(1, len(image) - 1):
        line = []

        for col in range(1, len(image[0]) - 1):
            pixels = [image[r][c] for r, c in get_neighbor_indices(row, col)]
            pixels = ''.join(pixels)
            idx = int(pixels.replace(".", "0").replace("#", "1"), 2)

            line.append(enhancement_lookup[idx])

        enhanced.append(''.join(line))

    return enhanced


def compute_new_background(current_background: str, lookup: str) -> str:
    idx = int(current_background.replace(".", "0").replace("#", "1") * 9, 2)
    return lookup[idx]


def enhance_for(data: Data, num_steps: int) -> int:
    lookup = data.enhancement_lookup

    background = "."
    image = data.image

    for _ in range(num_steps):
        image = add_background(image, background, delta=2)
        image = enhance_image(image, lookup)
        background = compute_new_background(background, lookup)

    num_lit_pixels = 0

    for line in image:
        num_lit_pixels += line.count("#")

    return num_lit_pixels


def solve_part_one(data: Data) -> int:
    return enhance_for(data, num_steps=2)


def solve_part_two(data: Data) -> int:
    return enhance_for(data, num_steps=50)


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 35
            assert solve_part_two(data) == 3351

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
