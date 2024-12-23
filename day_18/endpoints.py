from pathlib import Path
from typing import List

from fastapi import APIRouter

from day_16.endpoints import (
    PathFinderPuzzle,
    LocationCosting,
    rotate_clockwise,
    rotate_anticlockwise,
)
from day_6.endpoints import out_of_bounds
from utils import TaskInputWithMapDimensions, Direction, get_next_position, read_file

day_18_routes = APIRouter()


class Day18Pt1Input(TaskInputWithMapDimensions):
    first: int


def get_possible_moves(costing: LocationCosting, maze: List[str], cols, rows):
    """
    Get the possible moves and costs associated with them
    :param costing: the location costing to analyse
    :param maze: the map
    :return: a set of location costings to add to the list
    """
    position_in_front = get_next_position(costing.coordinate, costing.direction)
    moves: List[LocationCosting] = []
    if (
        not out_of_bounds(position_in_front, cols, rows)
        and maze[position_in_front[0]][position_in_front[1]] != "#"
    ):
        moves.append(
            LocationCosting(
                position_in_front,
                costing.direction,
                costing.cost + 1,
                costing.previous_positions,
            )
        )

    moves.extend(
        (
            LocationCosting(
                costing.coordinate,
                rotate_clockwise(costing.direction),
                costing.cost,
                costing.previous_positions,
            ),
            LocationCosting(
                costing.coordinate,
                rotate_anticlockwise(costing.direction),
                costing.cost,
                costing.previous_positions,
            ),
        )
    )

    return moves


def solve_map(escape_map, task_input):
    puzzle_info = PathFinderPuzzle((task_input.rows - 1, task_input.cols - 1))
    puzzle_info.add_location(LocationCosting((0, 0), Direction.NORTH, 0, set()))
    while True:
        location = puzzle_info.get_cheapest_location("estimated_cost")
        location_costing = puzzle_info.locations[location]
        location_costing.explored = True
        if location_costing.coordinate == puzzle_info.goal:
            return location_costing
        moves = get_possible_moves(
            location_costing, escape_map, task_input.rows, task_input.cols
        )
        for move in moves:
            puzzle_info.add_location(move)

        location_costing.explored = True


@day_18_routes.post("/1")
async def task_1(task_input: Day18Pt1Input):
    escape_map_cells = [
        ["." for _ in range(task_input.cols)] for _ in range(task_input.rows)
    ]

    for line in task_input.data.splitlines()[: task_input.first]:
        col, row = map(int, line.split(","))
        escape_map_cells[row][col] = "#"

    escape_map = ["".join(line) for line in escape_map_cells]

    return {"answer": solve_map(escape_map, task_input).cost}


@day_18_routes.post("/2")
def task_2(task_input: TaskInputWithMapDimensions):
    escape_map_cells = [
        ["." for _ in range(task_input.cols)] for _ in range(task_input.rows)
    ]

    obstacles = []
    for line in task_input.data.splitlines():
        col, row = map(int, line.split(","))
        obstacles.append((col, row))

    escape_map = ["".join(line) for line in escape_map_cells]
    location = solve_map(escape_map, task_input)

    for obstacle in obstacles:
        escape_map_cells[obstacle[0]][obstacle[1]] = "#"
        if obstacle in location.previous_positions:
            print("Need to rerun simulation")
            escape_map = ["".join(line) for line in escape_map_cells]
            try:
                location = solve_map(escape_map, task_input)
            except ValueError:
                break
        else:
            print(
                "No need to rerun simulation, as obstacle does not affect existing path!"
            )

    return {"answer": f"{obstacle[0]},{obstacle[1]}"}


if __name__ == "__main__":
    response = task_2(
        TaskInputWithMapDimensions(
            data=read_file(Path(__file__).parent.joinpath("test_input.txt").absolute()),
            rows=71,
            cols=71,
        )
    )
