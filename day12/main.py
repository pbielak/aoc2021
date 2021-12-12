"""Day 12 - Advent of Code"""
from __future__ import annotations

import os
from typing import Dict, List, Optional, Set, Tuple

Cave = str
Edge = Tuple[Cave, Cave]
Data = List[Edge]
Path = Tuple[Cave, ...]


def read_data(filename: str) -> Data:
    data = []
    with open(filename, "r") as fin:
        for line in fin.readlines():
            src_cave, dst_cave = tuple(line.strip().split("-"))
            data.append((src_cave, dst_cave))

        return data


def is_small_cave(cave: str) -> bool:
    return cave.lower() == cave


def get_caves_after_start(edges: Data) -> Set[Cave]:
    caves_after_start = set()

    for edge in edges:
        if edge[0] == "start":
            caves_after_start.add(edge[1])
        elif edge[1] == "start":
            caves_after_start.add(edge[0])

    return caves_after_start


def get_all_small_caves(edges: Data) -> Set[Cave]:
    small_caves = set()

    for edge in edges:
        if is_small_cave(edge[0]) and edge[0] not in ("start", "end"):
            small_caves.add(edge[0])
        elif is_small_cave(edge[1]) and edge[1] not in ("start", "end"):
            small_caves.add(edge[1])

    return small_caves


def generate_all_paths(
    edges: Data,
    allow_visit_small_cave_twice: bool = False,
) -> List[Path]:
    caves_after_start = get_caves_after_start(edges)

    if allow_visit_small_cave_twice:
        allowed_small_caves = get_all_small_caves(edges)
    else:
        allowed_small_caves = {None}

    paths = []

    for cave in caves_after_start:
        for allowed_small_cave in allowed_small_caves:
            if is_small_cave(cave):
                avsc = {cave: 1}
            else:
                avsc = {}

            ps = generate_path_recursively(
                edges=edges,
                current_path=("start", cave),
                already_visited_small_caves=avsc,
                small_cave_can_be_visited_twice=allowed_small_cave,
            )
            paths.extend(ps)

    paths = list(set(paths))

    return paths


def can_be_visited(
    cave: Cave,
    already_visited_small_caves: Dict[Cave, int],
    small_cave_can_be_visited_twice: Optional[Cave],
) -> bool:
    if cave == "start":
        return False

    num_visited = already_visited_small_caves.get(cave, 0)

    if small_cave_can_be_visited_twice is None:
        return num_visited == 0
    else:
        if cave == small_cave_can_be_visited_twice:
            return num_visited in (0, 1)
        else:
            return num_visited == 0


def generate_path_recursively(
    edges: Data,
    current_path: Path,
    already_visited_small_caves: Dict[Cave, int],
    small_cave_can_be_visited_twice: Optional[Cave],
) -> List[Path]:
    last_cave = current_path[-1]
    next_possible_caves = set()

    for edge in edges:
        # Consider edges like `(last_cave, *)`
        if (
            (last_cave == edge[0])
            and can_be_visited(edge[1], already_visited_small_caves=already_visited_small_caves, small_cave_can_be_visited_twice=small_cave_can_be_visited_twice)
            #and (edge[1] not in already_visited_small_caves)
            #and (edge[1] != "start")
        ):
            next_possible_caves.add(edge[1])
        # Consider edges like `(*, last_cave)`
        elif (
            (last_cave == edge[1])
            and can_be_visited(edge[0], already_visited_small_caves=already_visited_small_caves, small_cave_can_be_visited_twice=small_cave_can_be_visited_twice)
            #and (edge[0] not in already_visited_small_caves)
            #and (edge[0] != "start")
        ):
            next_possible_caves.add(edge[0])

    paths = []
    for next_cave in next_possible_caves:
        if next_cave == "end":
            paths.append((*current_path, "end"))
            continue

        if is_small_cave(next_cave):
            if small_cave_can_be_visited_twice is None:
                avsc = {**already_visited_small_caves, next_cave: 1}
            else:
                avsc = already_visited_small_caves.copy()
                avsc[next_cave] = avsc.get(next_cave, 0) + 1
        else:
            avsc = already_visited_small_caves

        paths.extend(
            generate_path_recursively(
                edges=edges,
                current_path=(*current_path, next_cave),
                already_visited_small_caves=avsc,
                small_cave_can_be_visited_twice=small_cave_can_be_visited_twice,
            )
        )

    return paths


def solve_part_one(data: Data) -> int:
    all_paths = generate_all_paths(edges=data)
    return len(all_paths)


def solve_part_two(data: Data) -> int:
    all_paths = generate_all_paths(
        edges=data,
        allow_visit_small_cave_twice=True,
    )
    return len(all_paths)


def run_tests():
    # Part 1
    print("Part 1 - tests")

    # Mini example 1
    mini_example_1 = [
        ("start", "A"),
        ("start", "b"),
        ("A", "c"),
        ("A", "b"),
        ("b", "d"),
        ("A", "end"),
        ("b", "end"),
    ]
    mini_example_1_res = generate_all_paths(edges=mini_example_1)
    mini_example_1_expected = [
        ("start", "A", "b", "A", "c", "A", "end"),
        ("start", "A", "b", "A", "end"),
        ("start", "A", "b", "end"),
        ("start", "A", "c", "A", "b", "A", "end"),
        ("start", "A", "c", "A", "b", "end"),
        ("start", "A", "c", "A", "end"),
        ("start", "A", "end"),
        ("start", "b", "A", "c", "A", "end"),
        ("start", "b", "A", "end"),
        ("start", "b", "end"),
    ]
    assert len(mini_example_1_res) == 10
    assert all(path in mini_example_1_expected for path in mini_example_1_res)
    print("Mini example 1 test passed ...")

    # Mini example 2
    mini_example_2 = [
        ("dc", "end"),
        ("HN", "start"),
        ("start", "kj"),
        ("dc", "start"),
        ("dc", "HN"),
        ("LN", "dc"),
        ("HN", "end"),
        ("kj", "sa"),
        ("kj", "HN"),
        ("kj", "dc"),
    ]
    mini_example_2_res = generate_all_paths(edges=mini_example_2)
    mini_example_2_expected = [
        ("start", "HN", "dc", "HN", "end"),
        ("start", "HN", "dc", "HN", "kj", "HN", "end"),
        ("start", "HN", "dc", "end"),
        ("start", "HN", "dc", "kj", "HN", "end"),
        ("start", "HN", "end"),
        ("start", "HN", "kj", "HN", "dc", "HN", "end"),
        ("start", "HN", "kj", "HN", "dc", "end"),
        ("start", "HN", "kj", "HN", "end"),
        ("start", "HN", "kj", "dc", "HN", "end"),
        ("start", "HN", "kj", "dc", "end"),
        ("start", "dc", "HN", "end"),
        ("start", "dc", "HN", "kj", "HN", "end"),
        ("start", "dc", "end"),
        ("start", "dc", "kj", "HN", "end"),
        ("start", "kj", "HN", "dc", "HN", "end"),
        ("start", "kj", "HN", "dc", "end"),
        ("start", "kj", "HN", "end"),
        ("start", "kj", "dc", "HN", "end"),
        ("start", "kj", "dc", "end"),
    ]
    assert len(mini_example_2_res) == 19
    assert all(path in mini_example_2_expected for path in mini_example_2_res)
    print("Mini example 2 test passed ...")

    # Part 2
    print("Part 2 - tests")

    # Mini example 1
    mini_example_1_res_p2 = generate_all_paths(
        edges=mini_example_1,
        allow_visit_small_cave_twice=True,
    )
    assert len(mini_example_1_res_p2) == 36
    print("Mini example 1 test passed ...")

    # Mini example 2
    mini_example_2_res_p2 = generate_all_paths(
        edges=mini_example_2,
        allow_visit_small_cave_twice=True,
    )
    assert len(mini_example_2_res_p2) == 103
    print("Mini example 2 test passed ...")


def main():
    run_tests()

    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 226
            assert solve_part_two(data) == 3_509

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
