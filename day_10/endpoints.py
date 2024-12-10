from typing import List, Set

from fastapi import APIRouter

from aoc_types import TaskInput, Coordinates

day_10_routes = APIRouter()


def find_trailheads(
    map_rows: List[str], row: int, col: int, trailheads: Set[Coordinates], start: int
):
    max_rows = len(map_rows)
    max_cols = len(map_rows[0])

    if start == 9:
        # Base case, we're at the summit!
        trailheads = trailheads.add((row, col))

    if col > 0 and map_rows[row][col - 1] == str(start + 1):
        # we need to look left!
        find_trailheads(map_rows, row, col - 1, trailheads, start + 1)

    if col < max_cols - 1 and map_rows[row][col + 1] == str(start + 1):
        # we need to look right!
        find_trailheads(map_rows, row, col + 1, trailheads, start + 1)

    if row > 0 and map_rows[row - 1][col] == str(start + 1):
        # we need to look up!
        find_trailheads(map_rows, row - 1, col, trailheads, start + 1)

    if row < max_rows - 1 and map_rows[row + 1][col] == str(start + 1):
        # we need to look down!
        find_trailheads(map_rows, row + 1, col, trailheads, start + 1)


def find_paths(map_rows: List[str], row: int, col: int, start: int):
    max_rows = len(map_rows)
    max_cols = len(map_rows[0])

    if start == 0:
        # Base case, we're at the summit!
        return 1

    total = 0

    if col > 0 and map_rows[row][col - 1] == str(start - 1):
        # we need to look left!
        total += find_paths(map_rows, row, col - 1, start - 1)

    if col < max_cols - 1 and map_rows[row][col + 1] == str(start - 1):
        # we need to look right!
        total += find_paths(map_rows, row, col + 1, start - 1)

    if row > 0 and map_rows[row - 1][col] == str(start - 1):
        # we need to look up!
        total += find_paths(map_rows, row - 1, col, start - 1)

    if row < max_rows - 1 and map_rows[row + 1][col] == str(start - 1):
        # we need to look down!
        total += find_paths(map_rows, row + 1, col, start - 1)

    return total


@day_10_routes.post("/1")
async def task_1(task_input: TaskInput):
    total = 0
    map_rows = task_input.data.splitlines()
    for i, row in enumerate(map_rows):
        for j, char in enumerate(row):
            if char == "0":
                trailheads = set()
                find_trailheads(map_rows, i, j, trailheads, 0)
                total += len(trailheads)
    return {"answer": total}


@day_10_routes.post("/2")
async def task_2(task_input: TaskInput):
    total = 0
    map_rows = task_input.data.splitlines()
    for i, row in enumerate(map_rows):
        for j, char in enumerate(row):
            if char == "9":
                total += find_paths(map_rows, i, j, 9)

    return {"answer": total}
