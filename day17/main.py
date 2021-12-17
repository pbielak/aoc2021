"""Day 17 - Advent of Code"""
from __future__ import annotations

from math import ceil, floor, sqrt
from typing import List, NamedTuple, Optional, Tuple


class Data(NamedTuple):
    x_min: int
    x_max: int

    y_min: int
    y_max: int


def will_hit_target(v_x: int, v_y: int, target: Data) -> bool:
    x, y = (0, 0)

    while True:
        # Update position
        x += v_x
        y += v_y

        # Update velocity
        if v_x != 0:
            v_x -= 1

        v_y -= 1

        # Check for hitting
        if (
            target.x_min <= x <= target.x_max
            and target.y_min <= y <= target.y_max
        ):
            return True

        # Check for missing
        if (
            (x < target.x_min and v_x == 0)
            or (y < target.y_min)  # Negative positions only
        ):
            return False


def solve(data: Data) -> Tuple[int, int]:
    # For a given v_x the following x positions are:
    # v_x, v_x + (v_x - 1), v_x + (v_x - 1) + (v_x - 2), ...
    # Hence the position x(t) = v_x * t - (t*(t-1)/2)
    # We are only interested in the first part of this parabola (as v_x stops
    # to decrease when 0 is reached)
    # The maximum position can be found by taking the derivative: x'(t) = 0
    # d/dt (-0.5t^2 + (v_x + 0.5)t) = 0
    # -t' + (v_x + 0.5) = 0
    # t' = v_x + 0.5
    # Next, we want to find the value x(t')
    # x(t') = -0.5*(v_x + 0.5)^2 + (v_x + 0.5) * (v_x + 0.5)
    # x(t') = -0.5*(v_x + 0.5)^2 + (v_x + 0.5)^2
    # x(t') = 0.5*(v_x + 0.5)
    # We need x(t') >= x_min, hence:
    # v_x_min = sqrt(2*x_min) - 0.5
    # On the other hand the maximum velocity: v_x_max = x_max
    v_x_min = ceil(sqrt(2 * data.x_min) - 0.5)
    v_x_max = data.x_max

    # Next, let's consider the motion on the Y axis
    # The minimum value is given when we directly shoot down at the target
    # (and do not optimize for the highest shot), i.e., v_y_min = y_min
    # To derive the maximum velocity, note that first the projectile is launched
    # upwards and it is again a series: v_y, v_y - 1, ..., 0. Hence, the
    # maximum height reached is: y_max = (v_y (v_y - 1)) / 2. Then, the velocity
    # starts to rise again: 0, 1, ..., v_y (when reaching y = 0), v_y + 1, ...
    # How to find the maximum v_y? The next step after reaching y = 0, must not
    # overshoot the target, i.e.: -(v_y + 1) <= y_min  (note y_min < 0).
    v_y_min = data.y_min
    v_y_max = -data.y_min + 1

    print(f"Grid: v_x = [{v_x_min};{v_x_max}], v_y = [{v_y_min};{v_y_max}]")

    best_y_max = 0
    hits = []
    for v_x in range(v_x_min, v_x_max + 1):
        for v_y in range(v_y_min, v_y_max + 1):
            y_max = (v_y * (v_y + 1)) // 2

            if will_hit_target(v_x=v_x, v_y=v_y, target=data):
                best_y_max = max(best_y_max, y_max)
                hits.append((v_x, v_y))

    return best_y_max, len(hits)


def main():
    cases = [
        ("example", Data(x_min=20, x_max=30, y_min=-10, y_max=-5)),
        ("input", Data(x_min=94, x_max=151, y_min=-156, y_max=-103)),
    ]

    for name, data in cases:
        y_max, num_hits = solve(data)

        if name == "example":
            assert y_max == 45
            assert num_hits == 112

        print(
            f"Case: {name}\n"
            f"* Part One: {y_max}\n"
            f"* Part Two: {num_hits}\n"
        )


if __name__ == "__main__":
    main()
