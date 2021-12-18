"""Day 18 - Advent of Code"""
from __future__ import annotations

from math import ceil, floor
import os
from typing import Callable, List, Optional, Union


Data = List[str]


def read_data(filename: str) -> Data:
    with open(filename, "r") as fin:
        return [line.strip() for line in fin.readlines()]


class Pair:

    def __init__(
        self,
        left: Union[int, Pair],
        right: Union[int, Pair],
        parent: Optional[Pair] = None,
    ):
        self.left = left
        self.right = right
        self.parent = parent

    def __eq__(self, other: Pair) -> bool:
        if not isinstance(other, Pair):
            return False

        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return f"({self.left}, {self.right})"

    def __add__(self, other: Pair) -> Pair:
        pair = Pair(parent=None, left=self, right=other)

        pair.left.parent = pair
        pair.right.parent = pair
        return pair

    def matches_predicate(self, predicate: Callable[[int], bool]) -> bool:
        if isinstance(self.left, int):
            res_left = predicate(self.left)
        else:
            res_left = self.left.matches_predicate(predicate)

        if isinstance(self.right, int):
            res_right = predicate(self.right)
        else:
            res_right = self.right.matches_predicate(predicate)

        return res_left or res_right

    def reduce(self) -> Pair:
        while True:
            if self.explode():
                continue

            if self.split():
                continue

            break

        return self

    def explode(self, current_depth: int = 0) -> bool:
        if current_depth != 4:
            exploded = False

            if isinstance(self.left, Pair):
                exploded = self.left.explode(current_depth + 1)

            if not exploded and isinstance(self.right, Pair):
                exploded = self.right.explode(current_depth + 1)
        else:
            apply_explode(self)
            exploded = True

        return exploded

    def split(self) -> bool:
        if isinstance(self.left, int):
            if self.left >= 10:
                self.left = _make_split_pair(self.left, parent=self)
                return True
        else:
            was_split = self.left.split()

            if was_split:
                return True

        if isinstance(self.right, int):
            if self.right >= 10:
                self.right = _make_split_pair(self.right, parent=self)
                return True
        else:
            was_split = self.right.split()

            if was_split:
                return True

        return False

    def magnitude(self) -> int:
        if isinstance(self.left, int):
            left_magnitude = self.left
        else:
            left_magnitude = self.left.magnitude()

        if isinstance(self.right, int):
            right_magnitude = self.right
        else:
            right_magnitude = self.right.magnitude()

        return 3 * left_magnitude + 2 * right_magnitude


def apply_explode(pair: Pair):
    # Propagate left value (if possible)
    _update_first_left_uncle(pair, pair.left)

    # Propagate right value (if possible)
    _update_first_right_uncle(pair, pair.right)

    # Replace current element with 0 in parent
    if id(pair.parent.left) == id(pair):
        pair.parent.left = 0
    else:
        assert id(pair.parent.right) == id(pair)
        pair.parent.right = 0


def _update_first_left_uncle(pair: Pair, value: int):
    current_pair = pair

    while current_pair.parent is not None:
        # We are the left element
        if id(current_pair) == id(current_pair.parent.left):
            current_pair = current_pair.parent
        # We are the right element
        elif id(current_pair) == id(current_pair.parent.right):
            if isinstance(current_pair.parent.left, int):
                current_pair.parent.left += value
                return
            else:
                pair = _get_parent_of_rightmost(current_pair.parent.left)
                pair.right += value
                return

    return


def _update_first_right_uncle(pair: Pair, value: int):
    current_pair = pair

    while current_pair.parent is not None:
        # We are the right element
        if id(current_pair) == id(current_pair.parent.right):
            current_pair = current_pair.parent
        # We are the left element
        elif id(current_pair) == id(current_pair.parent.left):
            if isinstance(current_pair.parent.right, int):
                current_pair.parent.right += value
                return
            else:
                pair = _get_parent_of_leftmost(current_pair.parent.right)
                pair.left += value
                return

    return


def _get_parent_of_leftmost(pair: Pair) -> Pair:
    while isinstance(pair.left, Pair):
        pair = pair.left

    return pair


def _get_parent_of_rightmost(pair: Pair) -> Pair:
    while isinstance(pair.right, Pair):
        pair = pair.right

    return pair


def _make_split_pair(value: int, parent: Pair) -> Pair:
    return Pair(left=floor(value / 2), right=ceil(value / 2), parent=parent)


def find_right_comma_idx(number: str) -> int:
    """Find the comma that separates the outermost pair."""
    num_opening_brackets = 0
    for idx in range(len(number)):
        if number[idx] == "," and num_opening_brackets == 0:
            return idx
        elif number[idx] == "[":
            num_opening_brackets += 1
        elif number[idx] == "]":
            num_opening_brackets -= 1


def is_digit(char: str) -> bool:
    return "0" <= char <= "9"


def parse(number: str, parent: Optional[Pair] = None) -> Pair:
    assert number[0] == "[" and number[-1] == "]"

    # Omit brackets
    number = number[1:-1]

    # Find the comma that divides the current pair into left and right
    comma_idx = find_right_comma_idx(number)
    left = number[:comma_idx]
    right = number[comma_idx + 1:]

    # We need to keep track of parents, so let's create the pair object, but
    # do not care right now about the typing
    pair = Pair(parent=parent, left=left, right=right)

    if all(is_digit(c) for c in left):
        pair.left = int(left)
    else:
        pair.left = parse(left, parent=pair)

    if all(is_digit(c) for c in right):
        pair.right = int(right)
    else:
        pair.right = parse(right, parent=pair)

    return pair


def add_all_numbers(numbers: List[str]) -> Pair:
    numbers = [parse(n) for n in numbers]

    total = numbers[0]

    for number in numbers[1:]:
        total = (total + number).reduce()

    return total


def solve_part_one(data: Data) -> int:
    total = add_all_numbers(numbers=data)
    return total.magnitude()


def solve_part_two(data: Data) -> int:
    pass


def run_tests():
    # Parsing tests
    assert parse("[1,2]") == Pair(1, 2)
    assert parse("[[1,2],3]") == Pair(Pair(1, 2), 3)
    assert parse("[9,[8,7]]") == Pair(9, Pair(8, 7))
    assert parse("[[1,9],[8,5]]") == Pair(Pair(1, 9), Pair(8, 5))

    # Addition tests
    assert parse("[1,2]") + parse("[[3,4],5]") == parse("[[1,2],[[3,4],5]]")

    # Explode tests
    e1 = parse("[[[[[9,8],1],2],3],4]")
    assert e1.explode() is True
    assert e1 == Pair(Pair(Pair(Pair(0, 9), 2), 3), 4)

    e2 = parse("[7,[6,[5,[4,[3,2]]]]]")
    assert e2.explode() is True
    assert e2 == Pair(7, Pair(6, Pair(5, Pair(7, 0))))

    e3 = parse("[[6,[5,[4,[3,2]]]],1]")
    assert e3.explode() is True
    assert e3 == Pair(Pair(6, Pair(5, Pair(7, 0))), 3)

    e4 = parse("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    assert e4.explode() is True
    assert e4 == Pair(
        Pair(3, Pair(2, Pair(8, 0))),
        Pair(9, Pair(5, Pair(4, Pair(3, 2))))
    )
    assert e4.explode() is True
    assert e4 == Pair(
        Pair(3, Pair(2, Pair(8, 0))),
        Pair(9, Pair(5, Pair(7, 0)))
    )

    # Test split
    s1 = parse("[[[[0,7],4],[15,[0,13]]],[1,1]]")
    assert s1.split() is True
    assert s1 == Pair(
        Pair(
            Pair(
                Pair(0, 7),
                4,
            ),
            Pair(
                Pair(7, 8),
                Pair(0, 13),
            )
        ),
        Pair(1, 1)
    )

    # Test addition full example
    left = parse("[[[[4,3],4],4],[7,[[8,4],9]]]")
    right = parse("[1,1]")

    total = parse("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    after_explode_1 = parse("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
    after_explode_2 = parse("[[[[0,7],4],[15,[0,13]]],[1,1]]")
    after_split_1 = parse("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
    after_split_2 = parse("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
    after_explode_3 = parse("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

    assert left + right == total

    assert total.explode() is True
    assert total == after_explode_1

    assert after_explode_1.explode() is True
    assert after_explode_1 == after_explode_2

    assert after_explode_2.split() is True
    assert after_explode_2 == after_split_1

    assert after_split_1.split() is True
    assert after_split_1 == after_split_2

    assert after_split_2.explode() is True
    assert after_split_2 == after_explode_3

    # Test reduce
    left = parse("[[[[4,3],4],4],[7,[[8,4],9]]]")
    right = parse("[1,1]")
    assert (left + right).reduce() == after_explode_3

    # Multiple numbers addition test
    numbers = [
        "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
        "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
        "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
        "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
        "[7,[5,[[3,8],[1,4]]]]",
        "[[2,[2,2]],[8,[8,1]]]",
        "[2,9]",
        "[1,[[[9,3],9],[[9,0],[0,7]]]]",
        "[[[5,[7,4]],7],1]",
        "[[[[4,2],2],6],[8,7]]",
    ]
    total = add_all_numbers(numbers)
    expected_total = parse("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")

    assert total == expected_total

    # Magnitude tests
    assert parse("[9,1]").magnitude() == 29
    assert parse("[1,9]").magnitude() == 21
    assert parse("[[9,1],[1,9]]").magnitude() == 129


def main():
    run_tests()

    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Test cases
        if filename == "example.txt":
            assert solve_part_one(data) == 4140
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
