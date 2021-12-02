"""Day 2 - Advent of Code"""
from abc import abstractmethod
import os
from typing import List, NamedTuple


class Position(NamedTuple):
    x: int
    y: int


class Command:

    def __init__(self, value: int):
        self._value = value

    @abstractmethod
    def update_position(self, position: Position) -> Position:
        pass

    @staticmethod
    def from_str(command: str) -> "Command":
        commands = {
            "forward": Forward,
            "up": Up,
            "down": Down,
        }

        name, value = command.split(" ")

        if name not in commands.keys():
            raise KeyError(f"Unknown command: '{name}'")

        return commands[name](value=int(value))


class Forward(Command):

    def update_position(self, position: Position) -> Position:
        return Position(x=position.x + self._value, y=position.y)


class Up(Command):

    def update_position(self, position: Position) -> Position:
        return Position(x=position.x, y=position.y - self._value)


class Down(Command):

    def update_position(self, position: Position) -> Position:
        return Position(x=position.x, y=position.y + self._value)


def read_data(filename: str) -> List[Command]:
    with open(filename, "r") as fin:
        return [Command.from_str(line) for line in fin.readlines()]


def solve_part_one(data: List[Command]) -> int:
    position = Position(x=0, y=0)

    for command in data:
        position = command.update_position(position)

    return position.x * position.y


def main():
    files = ["example.txt", "input.txt"]

    for filename in files:
        data = read_data(os.path.join("data", filename))

        # Part 1
        solution_one = solve_part_one(data)

        print(
            f"File: {filename}\n"
            f"* Part One: {solution_one}\n"
        )


if __name__ == "__main__":
    main()
