import re
from typing import List, Tuple

from fastapi import APIRouter

from aoc_types import TaskInput

day_13_routes = APIRouter()


class ButtonPuzzle:
    button_a = None
    button_b = None
    target = None

    def __str__(self):
        return f"Target: {self.target}\nButton A: {self.button_a}\nButton B: {self.button_b}"


def get_button_vector(line: str) -> Tuple[int, int]:
    x, y = map(int, re.findall(r"\d+", line))
    return x, y


def build_puzzle(puzzle_string):
    puzzle = ButtonPuzzle()
    puzzle_string_components = puzzle_string.split("\n")
    puzzle.button_a = get_button_vector(puzzle_string_components[0])
    puzzle.button_b = get_button_vector(puzzle_string_components[1])
    puzzle.target = get_button_vector(puzzle_string_components[2])
    return puzzle


def process_input(task_input: str) -> List[ButtonPuzzle]:
    puzzle_list = []
    for puzzle_string in task_input.split("\n\n"):
        puzzle = build_puzzle(puzzle_string)
        puzzle_list.append(puzzle)

    return puzzle_list


def build_puzzle_task_2(puzzle_string):
    puzzle = ButtonPuzzle()
    puzzle_string_components = puzzle_string.split("\n")
    puzzle.button_a = get_button_vector(puzzle_string_components[0])
    puzzle.button_b = get_button_vector(puzzle_string_components[1])
    puzzle.target = get_button_vector(puzzle_string_components[2])
    puzzle.target = (
        puzzle.target[0] + 10000000000000,
        puzzle.target[1] + 10000000000000,
    )
    return puzzle


def process_input_task_2(task_input: str) -> List[ButtonPuzzle]:
    puzzle_list = []
    for puzzle_string in task_input.split("\n\n"):
        puzzle = build_puzzle_task_2(puzzle_string)
        puzzle_list.append(puzzle)

    return puzzle_list


def solve_puzzle(puzzle):
    x1, x2 = puzzle.button_a
    y1, y2 = puzzle.button_b
    z1, z2 = puzzle.target
    # for vectors 'x' and 'y', we press 'x' 'a' times and 'y' 'b' times to get to the end
    # ax + by = z
    # ax1 + by1 = z1
    # ax2 + by2 = z2
    # a = (z1 - by1) / x1
    # ((z1 - by1) / x1)x2 + by2 = z2
    # (x2z1 - bx2y1)/x1 + by2 = z2
    # x2z1 - bx2y1 + by2x1 = z2x1
    # by2x1 - bx2y1 = z2x1 - x2z1
    # b(y2x1 - x2y1) = z2x1 - x2z1
    # b = (z2x1 - x2z1) / (y2x1 - x2y1)
    b = (z2 * x1 - x2 * z1) / (y2 * x1 - x2 * y1)
    a = (z1 - b * y1) / x1

    return a, b


@day_13_routes.post("/1")
async def task_1(task_input: TaskInput):
    total = 0
    puzzles = process_input(task_input.data)
    for puzzle in puzzles:
        a, b = solve_puzzle(puzzle)

        if b.is_integer() and a.is_integer() and (a <= 100 and b <= 100):
            cost = 3 * a + b
            total += int(cost)

    return {"answer": total}


@day_13_routes.post("/2")
async def task_2(task_input: TaskInput):
    total = 0
    puzzles = process_input_task_2(task_input.data)
    for puzzle in puzzles:
        a, b = solve_puzzle(puzzle)
        if b.is_integer() and a.is_integer():
            cost = 3 * a + b
            total += int(cost)

    return {"answer": total}
