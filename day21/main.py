"""Day 21 - Advent of Code"""
from __future__ import annotations

import os
from typing import Generator, NamedTuple


class Data(NamedTuple):
    player_1_starting_position: int
    player_2_starting_position: int


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        p1_pos = int(fin.readline().split(":")[1].strip())
        p2_pos = int(fin.readline().split(":")[1].strip())
        return Data(
            player_1_starting_position=p1_pos,
            player_2_starting_position=p2_pos,
        )


def make_die(num_sides: int, step: int = 1) -> Generator[int, None, None]:
    while True:
        for i in range(1, num_sides + 1, step):
            yield i


def solve_part_one(data: Data) -> int:
    state = {
        "p1": {"score": 0, "pos": data.player_1_starting_position},
        "p2": {"score": 0, "pos": data.player_2_starting_position},
    }
    num_die_rolls = 0

    die = make_die(num_sides=100)

    while True:
        has_won = False
        looser = ""

        for p_name, p_state in state.items():
            move_delta = sum(next(die) for _ in range(3))

            new_pos = p_state["pos"] + move_delta
            while new_pos > 10:
                new_pos -= 10

            p_state["pos"] = new_pos
            p_state["score"] += new_pos
            num_die_rolls += 3

            if p_state["score"] >= 1_000:
                has_won = True
                looser = "p1" if p_name == "p2" else "p2"
                break

        if has_won:
            break

    looser_score = state[looser]["score"]

    answer = looser_score * num_die_rolls
    return answer


def solve_part_two(data: Data) -> int:
    pass


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 739_785
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
