import itertools
import math

from fastapi import APIRouter

from aoc_types import TaskInput
import numpy as np

day_4_routes = APIRouter()


def new_coords(x, y, angle):
    return x * math.cos(angle) - y * math.sin(angle), x * math.sin(
        angle
    ) + y * math.cos(angle)


def calculate_ending_location(rows, columns, line):
    new_rows = columns + rows - 1
    row = min([line + 1, rows]) - 1
    column = min([columns, new_rows - line]) - 1

    return row, column


def calculate_starting_location(rows, columns, line):
    new_rows = columns + rows - 1
    chars_in_row = get_chars_in_row(line, new_rows)

    starting_position = calculate_ending_location(rows, columns, line)

    row = starting_position[0] - chars_in_row + 1
    column = starting_position[1] - chars_in_row + 1

    return row, column


def get_chars_in_row(line, new_rows):
    return min(new_rows - line, line + 1)


def half_rotate(input_string):
    lines = input_string.splitlines()
    columns = len(lines[0])
    rows = len(lines)

    rotated = []

    new_rows = columns + rows - 1

    for i in range(new_rows):
        start_row, start_column = calculate_starting_location(rows, columns, i)

        new_line = [
            lines[start_row + i][start_column + i]
            for i in range(get_chars_in_row(i, new_rows))
        ]
        rotated.append(new_line)

    return "\n".join("".join(line) for line in rotated)


def square_rotate(input_string: str):
    return "\n".join(
        "".join(line)
        for line in np.rot90([list(line) for line in input_string.splitlines()])
    )


def get_number_of_xmas(data):
    total = 0
    for line in data.splitlines():
        total += line.count("XMAS")
        total += line.count("SAMX")
    return total


@day_4_routes.post("/1")
async def task_1(task_input: TaskInput):
    total = 0
    total += get_number_of_xmas(task_input.data)
    total += get_number_of_xmas(half_rotate(task_input.data))
    rotated_90_input = square_rotate(task_input.data)
    total += get_number_of_xmas(rotated_90_input)
    total += get_number_of_xmas(half_rotate(rotated_90_input))

    return {"answer": total}


@day_4_routes.post("/2")
async def task_2(task_input: TaskInput):
    total = 0

    wordsearch = task_input.data.splitlines()

    for i, j in itertools.product(
        range(1, len(wordsearch) - 1), range(1, len(wordsearch[0]) - 1)
    ):
        if wordsearch[i][j] == "A":
            matches = 0
            # look diagonally one way
            if wordsearch[i - 1][j - 1] + wordsearch[i][j] + wordsearch[i + 1][
                j + 1
            ] in ["MAS", "SAM"]:
                matches += 1
            # look diagonally the other way
            if wordsearch[i + 1][j - 1] + wordsearch[i][j] + wordsearch[i - 1][
                j + 1
            ] in ["MAS", "SAM"]:
                matches += 1

            if matches > 1:
                total += 1

    return {"answer": total}
