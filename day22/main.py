"""Day 22 - Advent of Code"""
from __future__ import annotations

import os
from typing import Generator, List, NamedTuple, Set, Tuple


Position = Tuple[int, int, int]


class Range(NamedTuple):
    start: int
    end: int

    @staticmethod
    def from_str(string: str) -> Range:
        start, end = string.split("=")[1].split("..")
        return Range(start=int(start), end=int(end))

    def length(self) -> int:
        return self.end - self.start + 1

    def intersects(self, other: Range) -> bool:
        left_match = self.start <= other.start <= self.end
        right_match = other.start <= self.start <= other.end
        return left_match or right_match

    def intersection(self, other: Range) -> Range:
        return Range(
            start=max(self.start, other.start),
            end=min(self.end, other.end),
        )

    def contains(self, other: Range) -> bool:
        return self.start <= other.start and other.end <= self.end


class Cuboid(NamedTuple):
    x: Range
    y: Range
    z: Range

    def size(self) -> int:
        return (
            self.x.length()
            * self.y.length()
            * self.z.length()
        )

    def intersects(self, other: Cuboid) -> bool:
        return (
            self.x.intersects(other.x)
            and self.y.intersects(other.y)
            and self.z.intersects(other.z)
        )

    def intersection(self, other: Cuboid) -> Cuboid:
        return Cuboid(
            x=self.x.intersection(other.x),
            y=self.y.intersection(other.y),
            z=self.z.intersection(other.z),
        )

    def __repr__(self):
        x = f"{self.x.start}..{self.x.end}"
        y = f"{self.y.start}..{self.y.end}"
        z = f"{self.z.start}..{self.z.end}"
        return f"Cuboid(x={x}, y={y}, z={z})"


class RebootStep(NamedTuple):
    mode: str
    cuboid: Cuboid


Data = List[RebootStep]


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        steps = []
        for idx, line in enumerate(fin.readlines()):
            mode, coordinate_ranges = line.strip().split(" ")

            xrange, yrange, zrange = coordinate_ranges.split(",")

            xrange = Range.from_str(xrange)
            yrange = Range.from_str(yrange)
            zrange = Range.from_str(zrange)

            steps.append(RebootStep(mode, Cuboid(xrange, yrange, zrange)))

        return steps


def is_in_region(
    reboot_step: RebootStep,
    xrange: Range = Range(-50, 50),
    yrange: Range = Range(-50, 50),
    zrange: Range = Range(-50, 50),
) -> bool:
    cuboid = reboot_step.cuboid
    valid_xrange = (
            xrange.start <= cuboid.x.start
            and cuboid.x.end <= xrange.end
    )
    valid_yrange = (
            yrange.start <= cuboid.y.start
            and cuboid.y.end <= yrange.end
    )

    valid_zrange = (
            zrange.start <= cuboid.z.start
            and cuboid.z.end <= zrange.end
    )

    return valid_xrange and valid_yrange and valid_zrange


def count_active(reboot_steps: Data) -> int:
    cuboids = []

    for reboot_step in reboot_steps:
        current_cuboid = reboot_step.cuboid

        new_cuboids = []

        for existing_sign, existing_cuboid in cuboids:
            if existing_cuboid.intersects(current_cuboid):
                sign = -1 * existing_sign
                int_cuboid = existing_cuboid.intersection(current_cuboid)

                new_cuboids.append((sign, int_cuboid))

        cuboids.extend(new_cuboids)

        if reboot_step.mode == "on":
            cuboids.append((1, reboot_step.cuboid))

    num_active = 0

    for sign, cuboid in cuboids:
        num_active += sign * cuboid.size()

    return num_active


def solve_part_one(data: Data) -> int:
    return count_active(reboot_steps=[
        step
        for step in data
        if is_in_region(step)
    ])


def solve_part_two(data: Data) -> int:
    return count_active(reboot_steps=data)


def main():
    files = ["mini-example.txt", "example1.txt", "example2.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Part 1
        solution_one = solve_part_one(data)

        # Part 2
        solution_two = solve_part_two(data)

        # Test cases
        if filename == "mini-example.txt":
            assert solution_one == 39

        if filename == "example1.txt":
            assert solution_one == 590_784

        if filename == "example2.txt":
            assert solution_one == 474_140
            assert solution_two == 2_758_514_936_282_235

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
