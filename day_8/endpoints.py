import itertools
from collections import defaultdict

from fastapi import APIRouter

from aoc_types import TaskInput, Coordinates

day_8_routes = APIRouter()


def process_input(task_data: str):
    occupied_coordinates = set()
    tower_locations = defaultdict(set)

    for i, line in enumerate(split_input := (task_data.splitlines())):
        for j, char in enumerate(line):
            if char != ".":
                occupied_coordinates.add((i, j))
                tower_locations[char].add((i, j))

    total_rows = len(split_input)
    total_cols = len(split_input[0])

    return occupied_coordinates, tower_locations, total_rows, total_cols


def out_of_bounds(coordinates: Coordinates, grid_rows, grid_cols) -> bool:
    """
    Assess if a point is out of the boundaries of the grid
    :param coordinates: the location to check
    :param grid_rows: the height of the grid
    :param grid_cols: the width of the grid
    :return:
    """
    return (
        coordinates[0] >= grid_rows
        or coordinates[1] >= grid_cols
        or coordinates[0] < 0
        or coordinates[1] < 0
    )


@day_8_routes.post("/1")
async def task_1(task_input: TaskInput):
    occupied_coordinates, tower_locations, grid_rows, grid_cols = process_input(
        task_input.data
    )

    antinode_locations = set()

    for tower_location_set in tower_locations.values():
        combinations = itertools.combinations(tower_location_set, 2)
        for c in combinations:
            vertical_offset = c[0][0] - c[1][0]
            horizontal_offset = c[0][1] - c[1][1]
            antinode_1 = c[0][0] + vertical_offset, c[0][1] + horizontal_offset

            if not out_of_bounds(antinode_1, grid_rows, grid_cols):
                antinode_locations.add(antinode_1)

            antinode_2 = c[1][0] - vertical_offset, c[1][1] - horizontal_offset

            if not out_of_bounds(antinode_2, grid_rows, grid_cols):
                antinode_locations.add(antinode_2)

    return {"answer": len(antinode_locations)}


@day_8_routes.post("/2")
async def task_2(task_input: TaskInput):
    occupied_coordinates, tower_locations, grid_rows, grid_cols = process_input(
        task_input.data
    )

    antinode_locations = set()

    for tower_location_set in tower_locations.values():
        combinations = itertools.combinations(tower_location_set, 2)
        for c in combinations:
            horizontal_offset = c[0][1] - c[1][1]

            if horizontal_offset == 0:
                # it's a straight vertical line, so we would have an infinite gradient
                for i in range(grid_rows):
                    antinode_locations.add((i, c[0][1]))
            else:
                vertical_offset = c[0][0] - c[1][0]
                gradient = vertical_offset / horizontal_offset
                # go "backwards"
                i = 1
                while True:
                    i -= 1
                    new_col = c[0][1] + i
                    new_row = (i * gradient) + c[0][0]
                    if int(new_row) != new_row:
                        continue
                    potential_coordinate = (int(new_row), new_col)
                    if out_of_bounds(potential_coordinate, grid_rows, grid_cols):
                        break

                    antinode_locations.add(((int(new_row)), new_col))

                # go "forwards"
                i = 0
                while True:
                    i += 1
                    new_col = c[0][1] + i
                    new_row = (i * gradient) + c[0][0]
                    if int(new_row) != new_row:
                        continue
                    potential_coordinate = (int(new_row), new_col)
                    if out_of_bounds(potential_coordinate, grid_rows, grid_cols):
                        break

                    antinode_locations.add(((int(new_row)), new_col))

    return {"answer": len(antinode_locations)}
