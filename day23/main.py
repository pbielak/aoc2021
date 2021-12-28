"""Day 23 - Advent of Code"""
from __future__ import annotations

from functools import lru_cache
import sys
from typing import List, NamedTuple, Tuple

ENERGY_PER_STEP_2 = {"A": 1, "B": 10, "C": 100, "D": 1000}

ROOM_ENTRANCES = {"R1": 3, "R2": 5, "R3": 7, "R4": 9}

Position = Tuple[str, int]  # Either ("R[1-4]", int) or ("H", int)

Move = Tuple[Position, Position, int]


class State(NamedTuple):
    R1: Tuple[str, ...]
    R2: Tuple[str, ...]
    R3: Tuple[str, ...]
    R4: Tuple[str, ...]
    H: Tuple[str, ...]
    room_depth: int

    def is_done(self) -> bool:
        return (
            all(r1 == "A" for r1 in self.R1)
            and all(r2 == "B" for r2 in self.R2)
            and all(r3 == "C" for r3 in self.R3)
            and all(r4 == "D" for r4 in self.R4)
        )

    def get_positions_to_update(self) -> List[Position]:
        def _get_room(rtype: str, expected: str):
            room = [
                (c, idx + 1)
                for idx, c in enumerate(getattr(self, rtype))
            ]

            # Drop deepest amphipods that are in target room
            while len(room) > 0:
                if room[-1][0] == expected:
                    room = room[:-1]
                else:
                    break

            # Skip empty positions starting at room entrance
            while len(room) > 0:
                if room[0][0] == ".":
                    room = room[1:]
                else:
                    break

            if len(room) == 0:
                return []

            return [(rtype, room[0][1])]

        positions = [
            *_get_room("R1", "A"),
            *_get_room("R2", "B"),
            *_get_room("R3", "C"),
            *_get_room("R4", "D"),
            *[("H", i + 1) for i, h in enumerate(self.H) if h in "ABCD"]
        ]

        return positions

    def get_valid_moves(self) -> List[Move]:
        positions_to_update = self.get_positions_to_update()
        occupied_positions = self.all_occupied_positions()
        moves_to_consider = [
            move
            for move in get_all_possible_moves(self.room_depth)
            if (
                move[0] in positions_to_update
                and move[1] not in occupied_positions
            )
        ]
        out = []

        for src_pos, dst_pos, cost in moves_to_consider:
            atype = getattr(self, src_pos[0])[src_pos[1] - 1]
            final_cost = cost * ENERGY_PER_STEP_2[atype]

            if src_pos[0].startswith("R") and dst_pos[0] == "H":
                if not self.is_first_occupied_in_room(
                    position=src_pos[1],
                    room_type=src_pos[0],
                ):
                    continue

                if self.hallway_clear(ROOM_ENTRANCES[src_pos[0]], dst_pos[1]):
                    out.append((src_pos, dst_pos, final_cost))

            elif src_pos[0] == "H" and dst_pos[0].startswith("R"):
                if not self.can_enter_room(
                    amphipod_type=self.H[src_pos[1] - 1],
                    room_type=dst_pos[0],
                ):
                    continue

                if not self.is_first_unoccupied_in_room(
                    position=dst_pos[1],
                    room_type=dst_pos[0],
                ):
                    continue

                if self.hallway_clear(src_pos[1], ROOM_ENTRANCES[dst_pos[0]]):
                    out.append((src_pos, dst_pos, final_cost))
            else:
                raise RuntimeError(f"Unknown move type")

        return out

    def hallway_clear(self, source: int, destination: int) -> bool:
        """Checks whether amphipod can be moved along hallway"""

        if source < destination:  # Moving right
            start_idx = source + 1
            end_idx = destination
        else:  # Moving left
            start_idx = destination + 1
            end_idx = source

        return all(
            self.H[idx - 1] in (".", "x")
            for idx in range(start_idx, end_idx)
        )

    def can_enter_room(self, amphipod_type: str, room_type: str) -> bool:
        if not matches_room(amphipod_type, room_type):
            return False

        return all(
            matches_room(at, room_type)
            for at in getattr(self, room_type)
            if at != "."
        )

    def is_first_occupied_in_room(self, position: int, room_type: str) -> bool:
        room = getattr(self, room_type)
        return all(p == "." for p in room[:max(0, position - 1)])

    def is_first_unoccupied_in_room(self, position: int, room_type: str) -> bool:
        room = getattr(self, room_type)
        return all(p in "ABCD" for p in room[max(0, position - 1) + 1:])

    def all_occupied_positions(self) -> List[Position]:
        out = []

        for rtype in ("R1", "R2", "R3", "R4"):
            for depth in range(1, self.room_depth + 1):
                if getattr(self, rtype)[depth - 1] in "ABCD":
                    out.append((rtype, depth))

        for idx, h in enumerate(self.H):
            if h in "ABCD":
                out.append(("H", idx + 1))

        return out

    def apply_move(self, move: Move) -> State:
        state = {
            "R1": list(self.R1),
            "R2": list(self.R2),
            "R3": list(self.R3),
            "R4": list(self.R4),
            "H": list(self.H),
        }

        (src_rtype, src_pos), (dst_rtype, dst_pos), _ = move

        atype = state[src_rtype][src_pos - 1]

        state[src_rtype][src_pos - 1] = "."
        state[dst_rtype][dst_pos - 1] = atype

        state = {k: tuple(v) for k, v in state.items()}

        return State(**state, room_depth=self.room_depth)


def read_data(filename: str) -> State:
    if filename == "example.txt":
        return State(
            R1=("B", "A"),
            R2=("C", "D"),
            R3=("B", "C"),
            R4=("D", "A"),
            H=tuple("..x.x.x.x.."),
            room_depth=2,
        )

    elif filename == "input.txt":
        return State(
            R1=("A", "B"),
            R2=("C", "D"),
            R3=("C", "A"),
            R4=("D", "B"),
            H=tuple("..x.x.x.x.."),
            room_depth=2,
        )


def get_all_possible_moves(room_depth: int) -> List[Move]:
    out = []

    all_room_positions = [
        (rtype, pos)
        for rtype in ("R1", "R2", "R3", "R4")
        for pos in range(1, room_depth + 1)
    ]

    all_hallway_positions = [("H", i) for i in (1, 2, 4, 6, 8, 10, 11)]

    for room in all_room_positions:
        for hall in all_hallway_positions:
            d = distance(room, hall)
            out.append((room, hall, d))
            out.append((hall, room, d))

    return out


def distance(src: Position, dst: Position) -> int:
    """
    #############
    #...........#  Hallway
    ###.#.#.#.###
      #.#.#.#.#
      #########
       R R R R
       1 2 3 4
    """

    if src[0] == "H":  # Start in hallway
        if dst[0] == "H":  # Move inside the hallway
            return dst[1] - src[1]
        else:  # Move inside a room
            assert dst[0].startswith("R")
            return abs(src[1] - ROOM_ENTRANCES[dst[0]]) + dst[1]
    else:  # Start in a room
        assert src[0].startswith("R")

        if dst[0] == "H":  # Move into the hallway
            return src[1] + abs(ROOM_ENTRANCES[src[0]] - dst[1])
        else:  # Move into another room
            assert dst[0].startswith("R")
            return (
                src[1]
                + abs(ROOM_ENTRANCES[src[0]] - ROOM_ENTRANCES[dst[0]])
                + dst[1]
            )


def matches_room(amphipod_type: str, room_type: str) -> bool:
    if amphipod_type == "A":
        return room_type == "R1"

    if amphipod_type == "B":
        return room_type == "R2"

    if amphipod_type == "C":
        return room_type == "R3"

    assert amphipod_type == "D"
    return room_type == "R4"


@lru_cache(maxsize=None)
def get_min_moving_cost(state: State) -> Tuple[int, Tuple[str, ...]]:
    if state.is_done():
        return 0, ()

    best_cost = sys.maxsize
    best_actions = None

    valid_moves = state.get_valid_moves()

    if len(valid_moves) == 0:
        return sys.maxsize, ()

    for move in valid_moves:
        new_cost, new_actions = get_min_moving_cost(
            state=state.apply_move(move),
        )
        move_cost = move[2]

        if new_cost + move_cost < best_cost:
            best_cost = new_cost + move_cost
            best_actions = (str(move), *new_actions)

    return best_cost, best_actions


def solve_part_one(data: State) -> int:
    res = get_min_moving_cost(state=data)

    return res[0]


def transform_to_part_two(data: State) -> State:
    R1 = (data.R1[0], "D", "D", data.R1[1])
    R2 = (data.R2[0], "C", "B", data.R2[1])
    R3 = (data.R3[0], "B", "A", data.R3[1])
    R4 = (data.R4[0], "A", "C", data.R4[1])

    return State(R1=R1, R2=R2, R3=R3, R4=R4, H=data.H, room_depth=4)


def solve_part_two(data: State) -> int:
    res = get_min_moving_cost(state=transform_to_part_two(data))

    return res[0]


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
            assert solution_two == 44_169

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
