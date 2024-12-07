from collections import defaultdict
from copy import deepcopy
from enum import Enum
from typing import Tuple

from fastapi import APIRouter

from aoc_types import TaskInput

day_6_routes = APIRouter()


class Direction(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


def get_layout_info(task_input):
    guard_location = None
    obstacle_rows = defaultdict(set)
    obstacle_cols = defaultdict(set)
    lines = task_input.data.splitlines()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                # add row and column to sets
                obstacle_rows[i].add(j)
                obstacle_cols[j].add(i)
            elif char == "^":
                guard_location = (i, j)
    total_cols = len(lines[0])
    total_rows = len(lines)
    return guard_location, obstacle_cols, obstacle_rows, total_cols, total_rows


def find_obstacle_in_front_of_guard(
    obstacles, guard_location, backup_value, increasing
) -> int:
    if guard_location[0] not in obstacles:
        return backup_value
    obstacles_in_line = obstacles[guard_location[0]]

    if increasing:
        return min(
            (o for o in obstacles_in_line if o > guard_location[1]),
            default=backup_value,
        )
    else:
        return max(
            (o for o in obstacles_in_line if o < guard_location[1]),
            default=backup_value,
        )


def find_north_obstacle(guard_location, obstacle_cols) -> int:
    return find_obstacle_in_front_of_guard(
        obstacle_cols, guard_location[::-1], -1, False
    )


def find_east_obstacle(guard_location, obstacle_rows, total_cols) -> int:
    return find_obstacle_in_front_of_guard(
        obstacle_rows, guard_location, total_cols, True
    )


def find_west_obstacle(guard_location, obstacle_rows) -> int:
    return find_obstacle_in_front_of_guard(obstacle_rows, guard_location, -1, False)


def find_south_obstacle(guard_location, obstacle_cols, total_rows) -> int:
    return find_obstacle_in_front_of_guard(
        obstacle_cols, guard_location[::-1], total_rows, True
    )


@day_6_routes.post("/1")
async def task_1(task_input: TaskInput):
    (
        guard_location,
        obstacle_cols,
        obstacle_rows,
        total_cols,
        total_rows,
    ) = get_layout_info(task_input)
    direction = Direction.NORTH

    footpath = set()

    # this better not get stuck in a loop!
    while True:
        if direction == Direction.NORTH:
            obstacle_location = find_north_obstacle(guard_location, obstacle_cols)
            end_spot = obstacle_location + 1
            for i in range(end_spot, guard_location[0] + 1):
                footpath.add((i, guard_location[1]))

            guard_location = (end_spot, guard_location[1])

            direction = Direction.EAST
            if obstacle_location == -1:
                # we're leaving
                break
        elif direction == Direction.SOUTH:
            obstacle_location = find_south_obstacle(
                guard_location, obstacle_cols, total_rows
            )
            end_spot = obstacle_location - 1

            for i in range(guard_location[0], end_spot + 1):
                footpath.add((i, guard_location[1]))

            guard_location = (end_spot, guard_location[1])
            direction = Direction.WEST
            if obstacle_location == total_rows:
                # we're leaving
                break
        elif direction == Direction.WEST:
            obstacle_location = find_west_obstacle(guard_location, obstacle_rows)
            end_spot = obstacle_location + 1

            for i in range(end_spot, guard_location[1] + 1):
                footpath.add((guard_location[0], i))

            guard_location = (guard_location[0], end_spot)
            direction = Direction.NORTH
            if obstacle_location == -1:
                # we're leaving
                break
        elif direction == Direction.EAST:
            obstacle_location = find_east_obstacle(
                guard_location, obstacle_rows, total_cols
            )
            end_spot = obstacle_location - 1
            for i in range(guard_location[1], end_spot + 1):
                footpath.add((guard_location[0], i))

            guard_location = (guard_location[0], end_spot)
            direction = Direction.SOUTH
            if obstacle_location == total_cols:
                # we're leaving
                break

    return {"answer": len(footpath)}


horizontal_offset = {
    Direction.NORTH: 0,
    Direction.EAST: 1,
    Direction.SOUTH: 0,
    Direction.WEST: -1,
}
vertical_offset = {
    Direction.NORTH: -1,
    Direction.EAST: 0,
    Direction.SOUTH: 1,
    Direction.WEST: 0,
}


def rotate_guard(direction):
    if direction == Direction.NORTH:
        return Direction.EAST
    if direction == Direction.EAST:
        return Direction.SOUTH
    if direction == Direction.SOUTH:
        return Direction.WEST
    if direction == Direction.WEST:
        return Direction.NORTH


Coordinates = Tuple[int, int]


def next_position(guard_position: Coordinates, direction: Direction) -> Coordinates:
    """
    Get the location of the guard's next step if she were to go forward
    :param guard_position: current position of the guard
    :param direction: the direction the guard is facing
    :return: the next step in the guard's path
    """
    return (
        guard_position[0] + vertical_offset[direction],
        guard_position[1] + horizontal_offset[direction],
    )


def out_of_bounds(coordinate: Coordinates, total_cols: int, total_rows: int) -> bool:
    """
    Check if a coordinate is outside the grid - this means we'll be leaving the area
    :param coordinate: the coordinate to check
    :param total_cols: the width of the grid
    :param total_rows: the height of the grid
    :return: if we're out of bounds or not
    """
    if coordinate[0] < 0 or coordinate[0] >= total_rows:
        return True
    elif coordinate[1] < 0 or coordinate[1] >= total_cols:
        return True
    else:
        return False


def check_for_loop(
    guard_location: Coordinates,
    direction: Direction,
    obstacle_rows: dict[int, set[int]],
    total_cols: int,
    total_rows: int,
) -> bool:
    """

    :param guard_location: initial location of guard in this area
    :param direction: the direction the guard is facing
    :param obstacle_rows: a dictionary of obstacles
    :param total_cols: edge of the grid horizontally
    :param total_rows: edge of the grid vertically
    :return: whether or not there is a loop
    """

    next_step = next_position(guard_location, direction)
    obstacle_rows[next_step[0]].add(next_step[1])
    hit_obstacles = set()

    # this better not get stuck in a loop!
    while True:
        next_step = next_position(guard_location, direction)

        if out_of_bounds(next_step, total_cols, total_rows):
            return False

        if next_step[1] in obstacle_rows[next_step[0]]:
            obstacle_hit = (*next_step, direction)

            if obstacle_hit in hit_obstacles:
                return True

            hit_obstacles.add(obstacle_hit)
            direction = rotate_guard(direction)
        else:
            guard_location = next_step


@day_6_routes.post("/2")
async def task_2(task_input: TaskInput):
    # The important thing to note is that we can catch a guard in a loop if they end up going down a path they have
    # already been down, in the same direction.
    # For this we need to log a set of directions that she has gone as well as the places she has gone.
    # For this, we just work out if it's hit the same obstacle from the same direction before or not!

    (
        guard_location,
        obstacle_cols,
        obstacle_rows,
        total_cols,
        total_rows,
    ) = get_layout_info(task_input)
    direction = Direction.NORTH

    new_obstacles = set()

    # still need footpath, can't put an obstacle somewhere the guard has already been!
    footpath = set()

    # this better not get stuck in a loop!
    while True:
        next_step = next_position(guard_location, direction)

        if out_of_bounds(next_step, total_cols, total_rows):
            break

        if next_step[1] in obstacle_rows[next_step[0]]:
            direction = rotate_guard(direction)

        else:
            if next_step not in footpath:
                # run simulation
                if check_for_loop(
                    (guard_location[0], guard_location[1]),
                    direction,
                    deepcopy(obstacle_rows),
                    total_cols,
                    total_rows,
                ):
                    new_obstacles.add(next_step)
            footpath.add(guard_location)
            guard_location = next_step

    return {"answer": len(new_obstacles)}
