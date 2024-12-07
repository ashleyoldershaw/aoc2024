import numpy as np
from fastapi import APIRouter

from aoc_types import TaskInput

day_7_routes = APIRouter()


def format_number_as_bits(value, length):
    return format(value, "b").zfill(length)


def format_number_in_base(base, value, length):
    return np.base_repr(value, base=base).zfill(length)


@day_7_routes.post("/1")
async def task_1(task_input: TaskInput):
    total = 0

    puzzles = task_input.data.splitlines()

    for puzzle in puzzles:
        raw_target, raw_numbers = puzzle.split(":")
        target = int(raw_target.strip())
        numbers = [
            int(n) for n in raw_numbers.strip().split(" ")
        ]  # make lower and upper bounds

        max_checks = 2 ** (len(numbers) - 1)
        solution_found = False
        for i in range(max_checks):
            operators = [
                "+" if bit == "0" else "*"
                for bit in format_number_in_base(2, i, len(numbers) - 1)
            ]
            running_total = numbers[0]
            for j in range(len(numbers) - 1):
                if operators[j] == "+":
                    running_total += numbers[j + 1]
                else:
                    running_total *= numbers[j + 1]
            if running_total == target:
                solution_found = True
                break
        if solution_found:
            total += target

    return {"answer": total}


@day_7_routes.post("/2")
async def task_2(task_input: TaskInput):
    total = 0

    operator = ["+", "*", "||"]

    puzzles = task_input.data.splitlines()

    for i, puzzle in enumerate(puzzles):
        raw_target, raw_numbers = puzzle.split(":")
        target = int(raw_target.strip())
        numbers = [
            int(n) for n in raw_numbers.strip().split(" ")
        ]  # make lower and upper bounds

        max_checks = 3 ** (len(numbers) - 1)
        solution_found = False
        for i in range(max_checks):
            operators = [
                operator[int(bit)]
                for bit in format_number_in_base(3, i, len(numbers) - 1)
            ]
            running_total = numbers[0]
            for j in range(len(numbers) - 1):
                if operators[j] == "+":
                    running_total += numbers[j + 1]
                elif operators[j] == "*":
                    running_total *= numbers[j + 1]
                else:
                    running_total = concatenate_numbers(running_total, numbers[j + 1])
                if running_total > target:
                    break

            if running_total == target:
                solution_found = True
                break
        if solution_found:
            total += target

    return {"answer": total}


def concatenate_numbers(before, after):
    return int(str(before) + str(after))
