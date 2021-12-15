"""Day 15 - Advent of Code"""
from __future__ import annotations

from copy import deepcopy
import heapq
import os
import sys
from typing import Dict, List, Tuple


Position = Tuple[int, int]
Adj = Dict[Position, List[Position]]
Weights = Dict[Position, int]
Data = List[List[int]]


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        return [
            [int(risk_level) for risk_level in line.strip()]
            for line in fin.readlines()
        ]


def to_adj(data: Data) -> Tuple[Adj, Weights]:
    adj = {}
    weights = {}
    for x in range(len(data)):
        for y in range(len(data)):
            adj[(x, y)] = neighbors((x, y), size=len(data) - 1)
            weights[(x, y)] = data[x][y]

    return adj, weights


def neighbors(pos: Tuple[int, int], size: int) -> List[Tuple[int, int]]:
    n = [
        (pos[0], pos[1] - 1),
        (pos[0], pos[1] + 1),
        (pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
    ]

    return [
        (x, y)
        for (x, y) in n
        if 0 <= x <= size and 0 <= y <= size
    ]


class NodePriorityQueue:

    def __init__(self):
        self._nodes_pq = []

    def add(self, node: Position, weight: int):
        heapq.heappush(self._nodes_pq, (weight, node))

    def pop(self) -> Tuple[int, Position]:
        return heapq.heappop(self._nodes_pq)

    def __len__(self) -> int:
        return len(self._nodes_pq)


def dijkstra(
    adj: Adj,
    weights: Weights,
    start_pos: Position,
    target_pos: Position,
) -> Dict[Position, int]:
    """Based on `https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/`"""
    Q = NodePriorityQueue()

    dist = {}

    for v in adj.keys():
        dist[v] = sys.maxsize

    dist[start_pos] = 0
    Q.add(node=start_pos, weight=0)

    while len(Q) > 0:
        dist_u, u = Q.pop()

        if dist_u > dist[u]:
            continue

        if u == target_pos:
            break

        for v in adj[u]:
            alt = dist_u + weights[v]
            if alt < dist[v]:
                dist[v] = alt
                Q.add(node=v, weight=alt)

    return dist


def solve_part_one(data: Data) -> int:
    target_position = (len(data) - 1, len(data) - 1)

    adj, weights = to_adj(data)
    dist = dijkstra(
        adj=adj,
        weights=weights,
        start_pos=(0, 0),
        target_pos=target_position,
    )

    return dist[target_position]


def extend_tile_grid(data: Data, final_size: int = 5) -> Data:
    data = deepcopy(data)

    # Extend to the right
    for row in data:
        row.extend([
            value
            for delta in range(1, final_size)
            for value in increment_row_values(row, delta)
        ])

    # Extend below
    below_rows = []

    for delta in range(1, final_size):
        for row in data:
            below_rows.append(increment_row_values(row, delta))

    data.extend(below_rows)

    return data


def increment_row_values(row: List[int], delta: int) -> List[int]:
    def _increment(value: int) -> int:
        new_value = value + delta

        if new_value > 9:
            new_value -= 9

        return new_value

    return [_increment(v) for v in row]


def solve_part_two(data: Data) -> int:
    extended_grid = extend_tile_grid(data=data)
    target_position = (len(extended_grid) - 1, len(extended_grid) - 1)

    adj, weights = to_adj(data=extended_grid)
    dist = dijkstra(
        adj=adj,
        weights=weights,
        start_pos=(0, 0),
        target_pos=target_position,
    )

    return dist[target_position]


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 40
            assert solve_part_two(data) == 315

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
