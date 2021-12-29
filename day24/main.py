"""Day 24 - Advent of Code

The MONAD program consists of 14 repeating blocks of code, but different
constants are used in each block.

A single block can be written as the following code:

```py
def block(w: int, z: int) -> int:
    cond = (z % 26) + s1 == w
    z = z // div

    if cond:
        return z
    else:
        return z * 26 + (w + s2)
```

Note that such block is parameterized by three constants: `s1`, `div` and `s2`.
Each block denotes an operation performed for a single digit in the 14-digit
model number that we are looking for. In my input file, these three constants
are given as follows:

| Digit | s1 | div | s2 |
|     0 | 14 |   1 |  1 |
|     1 | 15 |   1 |  7 |
|     2 | 15 |   1 | 13 |
|     3 | -6 |  26 | 10 |  <---
|     4 | 14 |   1 |  0 |
|     5 | -4 |  26 | 13 |  <---
|     6 | 15 |   1 | 11 |
|     7 | 15 |   1 |  6 |
|     8 | 11 |   1 |  1 |
|     9 |  0 |  26 |  7 |  <---
|    10 |  0 |  26 | 11 |  <---
|    11 | -3 |  26 | 14 |  <---
|    12 | -9 |  26 |  4 |  <---
|    13 | -9 |  26 | 10 |  <---

We see that the number 26 appears multiple times in this task. Let's consider
`z` as a number written in base 26. Let's look again at the processing done by
a single block. The operation `z % 26` checks the value of the last digit of
the number `z` (base 26). If this last digit plus `s1` is equal to the current
digit `w` we enter the first branch of the if-statement.


Moreover, notice that we have only two options for the `div` parameter:

1) `div = 26`
- if the condition `cond` is satisfied -> drop the last digit of `z`
- else -> replace the last digit of `z` with `w + s2`

2) `div = 1`
- if the condition `cond` is satisfied -> no nothing
- else -> add `w + s2` as the last digit of `z`

If we want the MONAD check to be successful, i.e. the model number to be valid,
we need `z = 0` at the end of the whole process. To get `z = 0`, we need
each operation where `div = 26` to drop the last digit (and hence approach the
value `z = 0`). Dropping the last digit will be done only if the condition
`cond` is satisfied, i.e. the last digit of `z` plus `s1` is equal to the
current digit `w`.

In my case, this results in the following equations:

- The first `div = 26` row is for digit 3. We want digit 3 `w_3` to be equal to
the last digit of `z` which is equal to `w_2 + 13` plus `s1 = -6`, i.e.

`(w_2 + 13) - 6 = w_3`

- Next (digit 5), we have:

`(w_4 + 0) - 4 = w_5`

- Next (digit 9):

`(w_8 + 1) + 0 = w_9`

- Now for digit 10, the last digit of `z` is given by row `Digit 7`, i.e.

`(w_7 + 6) + 0 = w_10`

- In an analogous way, we obtain:

`(w_6 + 11) - 3 = w_11`
`(w_1 + 7) - 9 = w_12`
`(w_0 + 1) - 9 = w_13`


To sum up, for a model number to be valid we need to satisfy following equations:

`w_2 + 7 = w_3`
`w_4 - 4 = w_5`
`w_8 + 1 = w_9`
`w_7 + 6 = w_10`
`w_6 + 8 = w_11`
`w_1 - 2 = w_12`
`w_0 - 8 = w_13`

To find the largest model number we need to set the larger digit of each pair
to `9`, and to find the smallest one: the smaller one to `1`.

"""
from __future__ import annotations


def solve_part_one() -> int:
    # `w_2 + 7 = w_3`
    w_3 = 9
    w_2 = w_3 - 7

    # `w_4 - 4 = w_5`
    w_4 = 9
    w_5 = w_4 - 4

    # `w_8 + 1 = w_9`
    w_9 = 9
    w_8 = w_9 - 1

    # `w_7 + 6 = w_10`
    w_10 = 9
    w_7 = w_10 - 6

    # `w_6 + 8 = w_11`
    w_11 = 9
    w_6 = w_11 - 8

    # `w_1 - 2 = w_12`
    w_1 = 9
    w_12 = w_1 - 2

    # `w_0 - 8 = w_13`
    w_0 = 9
    w_13 = w_0 - 8

    digits = [
        w_0, w_1, w_2, w_3, w_4, w_5, w_6, w_7, w_8, w_9, w_10, w_11, w_12, w_13
    ]

    largest_number = int("".join(str(digit) for digit in digits))
    return largest_number


def solve_part_two() -> int:
    # `w_2 + 7 = w_3`
    w_2 = 1
    w_3 = w_2 + 7

    # `w_4 - 4 = w_5`
    w_5 = 1
    w_4 = w_5 + 4

    # `w_8 + 1 = w_9`
    w_8 = 1
    w_9 = w_8 + 1

    # `w_7 + 6 = w_10`
    w_7 = 1
    w_10 = w_7 + 6

    # `w_6 + 8 = w_11`
    w_6 = 1
    w_11 = w_6 + 8

    # `w_1 - 2 = w_12`
    w_12 = 1
    w_1 = w_12 + 2

    # `w_0 - 8 = w_13`
    w_13 = 1
    w_0 = w_13 + 8

    digits = [
        w_0, w_1, w_2, w_3, w_4, w_5, w_6, w_7, w_8, w_9, w_10, w_11, w_12, w_13
    ]

    smallest_number = int("".join(str(digit) for digit in digits))
    return smallest_number


def main():
    # Part 1
    solution_one = solve_part_one()

    # Part 2
    solution_two = solve_part_two()

    print(
        f"* Part One: {solution_one}\n"
        f"* Part Two: {solution_two}\n"
    )


if __name__ == "__main__":
    main()
