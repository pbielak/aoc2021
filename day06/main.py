"""Day 6 - Advent of Code"""
from __future__ import annotations


from functools import lru_cache
import os
from typing import List, Tuple

Data = List[int]

NEW_FISH_TIMER = 8
FISH_TIMER_AFTER_BREEDING = 6


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        return [int(timer) for timer in fin.readline().split(",")]


def simulate_fish_naive(data: Data, num_days: int) -> int:
    fish = data.copy()
    for _ in range(num_days):
        # Check for breeding fish
        num_new_fish = len([timer for timer in fish if timer == 0])

        # Update fish timers
        fish = [
            timer - 1 if timer != 0 else FISH_TIMER_AFTER_BREEDING
            for timer in fish
        ]

        # Add new fish
        fish.extend([NEW_FISH_TIMER] * num_new_fish)

    return len(fish)


def simulate_fish_with_day_skipping(data: Data, num_days: int) -> int:
    # At some point in the simulation, there are only zero day skips, so this
    # implementation degrades to the naive one
    fish = data.copy()
    day = 0

    while day != num_days:
        # Check how many days we can skip before next breeding
        num_days_without_breeding = min(fish)

        if num_days_without_breeding == 0:  # Breed
            num_new_fish = len([timer for timer in fish if timer == 0])
            diff = 1
        else:  # Skip few days
            num_new_fish = 0
            diff = num_days_without_breeding

        # Update fish timers
        fish = [
            timer - diff if timer != 0 else FISH_TIMER_AFTER_BREEDING
            for timer in fish
        ]

        # Add new fish
        fish.extend([NEW_FISH_TIMER] * num_new_fish)

        # Skip `diff` days
        day += diff

    return len(fish)


def simulate_fish_with_single_fish_analysis(data: Data, num_days: int) -> int:
    fish = data.copy()
    fish = [(0, timer) for timer in fish]

    num_total_fish = 0

    while fish:
        current_day, fish_timer = fish.pop(0)
        new_fish = generate_new_fish(current_day, num_days, fish_timer)

        num_total_fish += 1
        fish.extend(new_fish)

    return num_total_fish


def generate_new_fish(current_day: int, max_day: int, fish_timer: int) -> List[Tuple[int, int]]:
    new_fish = []

    breeding_day = current_day + fish_timer + 1

    if breeding_day > max_day:
        return []

    new_fish.append((breeding_day, NEW_FISH_TIMER))

    while True:
        breeding_day += FISH_TIMER_AFTER_BREEDING + 1

        if breeding_day > max_day:
            break

        new_fish.append((breeding_day, NEW_FISH_TIMER))

    return new_fish


def simulate_fish_using_recursive_function(data: Data, num_days: int) -> int:
    fish = data.copy()

    total = 0
    for fish_timer in fish:
        total += (
            # Count the fish we are currently considering....
            1
            # and the fish produced by it
            + compute_num_new_fish(day=0, max_day=num_days, fish_timer=fish_timer)
        )

    return total


@lru_cache(maxsize=None)
def compute_num_new_fish(day: int, max_day: int, fish_timer: int) -> int:
    if day == max_day:
        return 0

    if fish_timer == 0:
        return (
            1
            + compute_num_new_fish(day + 1, max_day, FISH_TIMER_AFTER_BREEDING)
            + compute_num_new_fish(day + 1, max_day, NEW_FISH_TIMER)
        )

    return compute_num_new_fish(day + 1, max_day, fish_timer - 1)


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert simulate_fish_naive(data, num_days=18) == 26
            assert simulate_fish_with_day_skipping(data, num_days=18) == 26
            assert simulate_fish_with_single_fish_analysis(data, num_days=18) == 26
            assert simulate_fish_using_recursive_function(data, num_days=18) == 26

            assert simulate_fish_naive(data, num_days=80) == 5_934
            assert simulate_fish_with_day_skipping(data, num_days=80) == 5_934
            assert simulate_fish_with_single_fish_analysis(data, num_days=80) == 5_934
            assert simulate_fish_using_recursive_function(data, num_days=80) == 5_934

            # The first three implementations take way too long...
            # assert simulate_fish_naive(data, num_days=256) == 26_984_457_539
            # assert simulate_fish_with_day_skipping(data, num_days=256) == 26_984_457_539
            # assert simulate_fish_with_single_fish_analysis(data, num_days=256) == 26_984_457_539
            assert simulate_fish_using_recursive_function(data, num_days=256) == 26_984_457_539

        # Part 1
        solution_one = simulate_fish_naive(data, num_days=80)

        # Part 2
        solution_two = simulate_fish_using_recursive_function(data, num_days=256)

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
