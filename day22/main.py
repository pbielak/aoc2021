"""Day 22 - Advent of Code"""
from __future__ import annotations

from dataclasses import dataclass
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


@dataclass
class RebootStep:
    mode: str
    xrange: Range
    yrange: Range
    zrange: Range

    def execute(self, reactor: Set[Position]) -> Set[Position]:
        _reactor = reactor.copy()

        for position in self._generate_positions():
            if self.mode == "on":
                _reactor.add(position)
            else:
                _reactor.discard(position)

        return _reactor

    def _generate_positions(self) -> Generator[Position, None, None]:
        for x in range(self.xrange.start, self.xrange.end + 1):
            for y in range(self.yrange.start, self.yrange.end + 1):
                for z in range(self.zrange.start, self.zrange.end + 1):
                    yield x, y, z


Data = List[RebootStep]


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        steps = []
        for line in fin.readlines():
            mode, coordinate_ranges = line.strip().split(" ")

            xrange, yrange, zrange = coordinate_ranges.split(",")

            xrange = Range.from_str(xrange)
            yrange = Range.from_str(yrange)
            zrange = Range.from_str(zrange)

            steps.append(RebootStep(mode, xrange, yrange, zrange))

        return steps


def is_in_region(
    reboot_step: RebootStep,
    xrange: Range = Range(-50, 50),
    yrange: Range = Range(-50, 50),
    zrange: Range = Range(-50, 50),
) -> bool:
    valid_xrange = (
        xrange.start <= reboot_step.xrange.start
        and reboot_step.xrange.end <= xrange.end
    )
    valid_yrange = (
        yrange.start <= reboot_step.yrange.start
        and reboot_step.yrange.end <= yrange.end
    )

    valid_zrange = (
            zrange.start <= reboot_step.zrange.start
            and reboot_step.zrange.end <= zrange.end
    )

    return all(valid for valid in (valid_xrange, valid_yrange, valid_zrange))


def solve_part_one(data: Data) -> int:
    reactor = set()

    for reboot_step in data:
        if not is_in_region(reboot_step):
            continue

        reactor = reboot_step.execute(reactor)

    return len(reactor)


def solve_part_two(data: Data) -> int:
    pass


def main():
    files = ["mini-example.txt", "example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "mini-example.txt":
            assert solve_part_one(data) == 39

        if filename == "example.txt":
            assert solve_part_one(data) == 590_784
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
