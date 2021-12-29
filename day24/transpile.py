"""Day 24 - Advent of Code"""
from __future__ import annotations


def main():
    output_file = open("monad.py", "w")

    output_file.write("w = 0\nx = 0\ny = 0\nz = 0\n")
    current_digit = 0

    with open("original_monad.txt", "r") as fin:
        for line in fin.readlines():
            line = line.strip()

            args = line.split(" ")[1:]

            if line.startswith("inp"):
                output_file.write(f"\n# Digit {current_digit}\n{args[0]} = int(input())")
                current_digit += 1
            elif line.startswith("add"):
                output_file.write(f"{args[0]} += {args[1]}")
            elif line.startswith("mul"):
                output_file.write(f"{args[0]} *= {args[1]}")
            elif line.startswith("div"):
                output_file.write(f"{args[0]} /= {args[1]}")
            elif line.startswith("mod"):
                output_file.write(f"{args[0]} %= {args[1]}")
            elif line.startswith("eql"):
                output_file.write(f"{args[0]} = int({args[0]} == {args[1]})")
            else:
                raise ValueError(f"Unknown instruction: {line}")

            output_file.write("\n")

    output_file.close()


if __name__ == "__main__":
    main()
