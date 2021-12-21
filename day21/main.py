"""Day 21 - Advent of Code"""
from __future__ import annotations

from functools import lru_cache
import os
from typing import Generator, NamedTuple, Tuple


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


@lru_cache(maxsize=None)
def count_wins_with_universe_split(
    p1_score: int, p1_pos: int,
    p2_score: int, p2_pos: int,
    turn: str,
    p1_wins: int, p2_wins: int,
) -> Tuple[int, int]:
    _p1_wins = p1_wins
    _p2_wins = p2_wins

    if p1_score >= 21 or p2_score >= 21:
        return _p1_wins, _p2_wins

    # The Diract die gives a single outcome of 1, 2 or 3. When rolling it three
    # times, we get a total of:
    # 3 - once
    # 4 - three times
    # 5 - six times
    # 6 - seven times
    # 7 - six times
    # 8 - three times
    # 9 - once
    outcomes = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]

    for outcome, count in outcomes:
        if turn == "p1":
            _p1_pos = p1_pos + outcome
            while _p1_pos > 10:
                _p1_pos -= 10
            _p1_score = p1_score + _p1_pos

            if _p1_score >= 21:
                _p1_wins += count
                continue

            _p2_score = p2_score
            _p2_pos = p2_pos
        else:
            _p2_pos = p2_pos + outcome
            while _p2_pos > 10:
                _p2_pos -= 10
            _p2_score = p2_score + _p2_pos

            if _p2_score >= 21:
                _p2_wins += count
                continue

            _p1_score = p1_score
            _p1_pos = p1_pos

        p1w, p2w = count_wins_with_universe_split(
            p1_score=_p1_score, p1_pos=_p1_pos,
            p2_score=_p2_score, p2_pos=_p2_pos,
            turn="p1" if turn == "p2" else "p2",
            p1_wins=p1_wins, p2_wins=p2_wins,
        )
        _p1_wins += p1w * count
        _p2_wins += p2w * count

    return _p1_wins, _p2_wins


def solve_part_two(data: Data) -> int:
    p1_wins, p2_wins = count_wins_with_universe_split(
        p1_score=0, p1_pos=data.player_1_starting_position,
        p2_score=0, p2_pos=data.player_2_starting_position,
        turn="p1",
        p1_wins=0,
        p2_wins=0,
    )

    return max(p1_wins, p2_wins)


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 739_785
            assert solve_part_two(data) == 444_356_092_776_315

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
