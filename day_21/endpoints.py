from functools import cache
from operator import sub
import re

from fastapi import APIRouter

from aoc_types import TaskInput

day_21_routes: APIRouter = APIRouter()


@cache
def keypad_path_between_buttons(start, end):
    keypad_positions = {
        "0": (3, 1),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "A": (3, 2),
    }
    path = ""
    difference = tuple(map(sub, keypad_positions[end], keypad_positions[start]))
    # order from furthest to closest to the A button
    # that order is <, v, then ^, >
    safe_left = start not in ["A", "0"] or end not in ["1", "4", "7"]
    safe_down = start not in ["1", "4", "7"] or end not in ["A", "0"]
    if difference[1] < 0 and safe_left:
        path += "<" * abs(difference[1])
    if difference[0] > 0 and safe_down:
        path += "v" * difference[0]
    if difference[0] < 0:
        path += "^" * abs(difference[0])
    if difference[1] < 0 and not safe_left:
        path += "<" * abs(difference[1])
    if difference[1] > 0:
        path += ">" * difference[1]
    if difference[0] > 0 and not safe_down:
        path += "v" * difference[0]

    path += "A"
    return path


@cache
def direction_path_between_buttons(start, end):
    keypad_positions = {"<": (1, 0), "^": (0, 1), ">": (1, 2), "v": (1, 1), "A": (0, 2)}
    path = ""
    difference = tuple(map(sub, keypad_positions[end], keypad_positions[start]))
    safe_left = end != "<" or start in ["v", ">"]
    safe_up = start != "<"
    # order from furthest to closest to the A button
    # that order is <, v, then ^, >
    if difference[1] < 0 and safe_left:
        path += "<" * abs(difference[1])
    if difference[0] > 0:
        path += "v" * difference[0]
    if difference[1] < 0 and not safe_left:
        path += "<" * abs(difference[1])
    if difference[0] < 0 and safe_up:
        path += "^" * abs(difference[0])
    if difference[1] > 0:
        path += ">" * difference[1]
    if difference[0] < 0 and not safe_up:
        path += "^" * abs(difference[0])

    path += "A"
    return path


def get_keypad_path(code):
    path = keypad_path_between_buttons("A", code[0])
    for i in range(len(code) - 1):
        path += keypad_path_between_buttons(code[i], code[i + 1])
    return path


def get_direction_path(code, start_letter="A"):
    pathlist = [direction_path_between_buttons(start_letter, code[0])]
    pathlist.extend(
        direction_path_between_buttons(code[i], code[i + 1])
        for i in range(len(code) - 1)
    )
    return "".join(pathlist)


def get_number(line: str) -> int:
    return int(re.findall(r"\d+", line)[0])


@cache
def recursive_direction_path(keypad_path, robots_between, start_letter="A"):
    direction_path = get_direction_path(keypad_path, start_letter)

    if robots_between != 1:
        total = 0
        for i, d in enumerate(direction_path):
            start_letter = direction_path[i - 1] if i > 0 else "A"
            total += recursive_direction_path(d, robots_between - 1, start_letter)
        return total

    return len(direction_path)


def get_complexity(code, robots_between):
    keypad_path = get_keypad_path(code)

    direction_path = recursive_direction_path(keypad_path, robots_between)

    return direction_path * get_number(code)


@day_21_routes.post("/1")
async def task_1(task_input: TaskInput):
    codes = task_input.data.splitlines()
    total = 0
    for code in codes:
        complexity = get_complexity(code, 2)

        total += complexity
    return {"answer": total}


@day_21_routes.post("/2")
def task_2(task_input: TaskInput):
    codes = task_input.data.splitlines()
    total = 0
    for code in codes:
        complexity = get_complexity(code, 25)

        total += complexity
    return {"answer": total}
