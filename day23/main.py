"""Day 23 - Advent of Code"""
from __future__ import annotations

from functools import lru_cache
import sys
from typing import List, Tuple

ENERGY_PER_STEP = {"Amber": 1, "Bronze": 10, "Copper": 100, "Desert": 1000}

# We cannot move an amphipod onto an room entrance position in the hallway
ALL_HALLWAY_POSITIONS = tuple(("H", i) for i in (1, 2, 4, 6, 8, 10, 11))

ROOM_ENTRANCES = {"R1": 3, "R2": 5, "R3": 7, "R4": 9}

ALL_ROOM_POSITIONS = tuple(
    (f"R{i}", j) for i in range(1, 4 + 1) for j in range(1, 2 + 1)
)

Position = Tuple[str, int]  # Either ("R[1-4]", int) or ("H", int)
AmphipodType = str  # One of ["Amber", "Bronze", "Copper", "Desert"]

Amphipod = Tuple[AmphipodType, Position]

State = Tuple[Amphipod, ...]

Data = Tuple[State, State]


def read_data(filename: str) -> Data:
    if filename == "example.txt":
        # Amphipods that are already placed in the proper rooms and positions
        non_movable_amphipods = (
            ("Amber", ("R1", 2)),
            ("Copper", ("R3", 2)),
        )
        state = (
            ("Amber", ("R4", 2)),
            ("Bronze", ("R1", 1)), ("Bronze", ("R3", 1)),
            ("Copper", ("R2", 1)),
            ("Desert", ("R2", 2)), ("Desert", ("R4", 1)),
        )

        return non_movable_amphipods, state

    elif filename == "input.txt":
        non_movable_amphipods = ()
        state = (
            ("Amber", ("R1", 1)), ("Amber", ("R3", 2)),
            ("Bronze", ("R1", 2)), ("Bronze", ("R4", 2)),
            ("Copper", ("R2", 1)), ("Copper", ("R3", 1)),
            ("Desert", ("R2", 2)), ("Desert", ("R4", 1)),
        )

        return non_movable_amphipods, state


def distance(
    source: Position,
    destination: Position,
) -> int:
    """
    #############
    #...........#  Hallway
    ###.#.#.#.###
      #.#.#.#.#
      #########
       R R R R
       1 2 3 4
    """

    hallway_room_entrance_positions = {"R1": 3, "R2": 5, "R3": 7, "R4": 9}
    rooms = ["R1", "R2", "R3", "R4"]

    if source[0] == "H":  # Start in hallway
        if destination[0] == "H":  # Move inside the hallway
            return destination[1] - source[1]
        else:  # Move inside a room
            assert destination[0] in rooms
            return (
                abs(
                    source[1]
                    - hallway_room_entrance_positions[destination[0]]
                ) + destination[1]
            )
    else:  # Start in a room
        assert source[0] in rooms

        if destination[0] == "H":  # Move into the hallway
            return (
                source[1]
                + abs(
                    hallway_room_entrance_positions[source[0]]
                    - destination[1]
                )
            )
        else:  # Move into another room
            assert destination[0] in rooms
            return (
                source[1]
                + abs(
                    hallway_room_entrance_positions[source[0]]
                    - hallway_room_entrance_positions[destination[0]]
                )
                + destination[1]
            )


def matches_room(amphipod_type: AmphipodType, room_type: str) -> bool:
    if amphipod_type == "Amber":
        return room_type == "R1"

    if amphipod_type == "Bronze":
        return room_type == "R2"

    if amphipod_type == "Copper":
        return room_type == "R3"

    assert amphipod_type == "Desert"
    return room_type == "R4"


def is_end(state: State) -> bool:
    return all(
        matches_room(amphipod_type, room_type)
        for amphipod_type, (room_type, _) in state
    )


@lru_cache(maxsize=None)
def generate_all_possible_moves(
    non_movable_amphipods: State,
    state: State,
) -> List[Tuple[int, State, State, str]]:
    free_hall_positions = sorted(
        set(ALL_HALLWAY_POSITIONS)
        - set([pos for _, pos in state if pos[0] == "H"])
    )
    occupied_hall_positions = set([pos[1] for _, pos in state if pos[0] == "H"])

    taken_rooms = {
        **{pos: atype for atype, pos in non_movable_amphipods},
        **{pos: atype for atype, pos in state if pos[0].startswith("R")},
    }
    free_room_positions = {}
    for amphipod_type, room_type in (
        ("Amber", "R1"),
        ("Bronze", "R2"),
        ("Copper", "R3"),
        ("Desert", "R4"),
    ):
        free_room_positions[amphipod_type] = []

        if (room_type, 1) not in taken_rooms and (room_type, 2) not in taken_rooms:
            free_room_positions[amphipod_type] = [(room_type, 1), (room_type, 2)]

        if (room_type, 2) in taken_rooms and (room_type, 1) not in taken_rooms:
            if taken_rooms[(room_type, 2)] == amphipod_type:
                free_room_positions[amphipod_type].append((room_type, 1))

    out = []
    for idx in range(len(state)):
        prev = state[:idx]
        current = state[idx]
        following = state[idx + 1:]

        if current[1][0].startswith("R"):  # If current amphipod is in room
            can_be_moved = (
                (current[1][1] == 1)  # is first in room
                or (current[1][1] == 2 and (current[1][0], 1) not in taken_rooms)  # second in room, but first position is free
            )

            if not can_be_moved:
                continue

            for hpos in free_hall_positions:
                # Check for other amphipods in hallway
                if any(
                    (ROOM_ENTRANCES[current[1][0]] < oc < hpos[1])
                    or (hpos[1] < oc < ROOM_ENTRANCES[current[1][0]])
                    for oc in occupied_hall_positions
                ):
                    continue

                cost = distance(current[1], hpos) * ENERGY_PER_STEP[current[0]]
                new_state = (*prev, (current[0], hpos), *following)
                move = f"({current[0]}: {current[1]} -> {hpos}||{cost})"

                out.append((cost, non_movable_amphipods, new_state, move))

        else:  # If current amphipod is in hallway
            assert current[1][0] == "H"

            for rpos in free_room_positions[current[0]]:
                if rpos[1] == 1 and (rpos[0], 2) in free_room_positions[current[0]]:
                    continue

                # Check for other amphipods in hallway
                if any(
                    (ROOM_ENTRANCES[rpos[0]] < oc < current[1][1])
                    or (current[1][1] < oc < ROOM_ENTRANCES[rpos[0]])
                    for oc in occupied_hall_positions
                ):
                    continue

                cost = distance(current[1], rpos) * ENERGY_PER_STEP[current[0]]
                new_non_movable_amphipods = (*non_movable_amphipods, (current[0], rpos))
                new_state = (*prev, *following)
                move = f"({current[0]}: {current[1]} -> {rpos}||{cost})"

                out.append((cost, new_non_movable_amphipods, new_state, move))

    return out


@lru_cache(maxsize=None)
def get_min_moving_cost(
    non_movable_amphipods: State,
    state: State,
) -> Tuple[int, Tuple[str, ...]]:
    if is_end(state):
        return 0, ()

    best_cost = sys.maxsize
    best_actions = None

    all_possible_moves = generate_all_possible_moves(non_movable_amphipods, state)

    if len(all_possible_moves) == 0:
        return sys.maxsize, ()

    for step_cost, nma, ns, dbg in all_possible_moves:
        new_cost, new_actions = get_min_moving_cost(
            non_movable_amphipods=nma,
            state=ns,
        )

        if new_cost + step_cost < best_cost:
            best_cost = new_cost + step_cost
            best_actions = (dbg, *new_actions)

    return best_cost, best_actions


def solve_part_one(data: Data) -> int:
    res = get_min_moving_cost(
        non_movable_amphipods=data[0],
        state=data[1],
    )

    return res[0]


def solve_part_two(data: Data) -> int:
    pass


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(filename)

        # Part 1
        solution_one = solve_part_one(data)

        # Part 2
        solution_two = solve_part_two(data)

        # Test cases
        if filename == "example.txt":
            assert solution_one == 12_521
            assert solution_two == None

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
