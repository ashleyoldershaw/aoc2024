from collections import defaultdict
from enum import Enum

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


def find_obstacle_if_exists(
    initial_guard_location,
    prev_obstacle_cols,
    prev_obstacle_rows,
    total_cols,
    total_rows,
    start_direction,
):
    # basically keep going until either:
    # - we leave the map - no loop
    # - we hit something we've hit before - loop!

    direction = start_direction
    obstacles_hit = set()
    new_obstacle_coords = (
        initial_guard_location[0] + vertical_offset[direction],
        initial_guard_location[1] + horizontal_offset[direction],
    )

    new_obstacle_columns = defaultdict(set)
    new_obstacle_rows = defaultdict(set)
    for key, value in prev_obstacle_cols.items():
        new_obstacle_columns[key] = value.copy()
    for key, value in prev_obstacle_rows.items():
        new_obstacle_rows[key] = value.copy()

    new_obstacle_rows[new_obstacle_coords[0]].add(new_obstacle_coords[1])
    new_obstacle_columns[new_obstacle_coords[1]].add(new_obstacle_coords[0])

    guard_location = initial_guard_location

    # this better not get stuck in a loop!
    while True:
        if direction == Direction.NORTH:
            obstacle_location = find_north_obstacle(
                guard_location, new_obstacle_columns
            )
            end_spot = obstacle_location - vertical_offset[direction]

            if obstacle_location == -1:
                return False

            check_obstacle = (obstacle_location, guard_location[1], direction)
            if check_obstacle in obstacles_hit:
                return check_obstacle[:2]
            obstacles_hit.add(check_obstacle)

            guard_location = (end_spot, guard_location[1])
        elif direction == Direction.SOUTH:
            obstacle_location = find_south_obstacle(
                guard_location, new_obstacle_columns, total_rows
            )
            end_spot = obstacle_location - vertical_offset[direction]

            if obstacle_location == total_rows:
                return False

            check_obstacle = (obstacle_location, guard_location[1], direction)
            if check_obstacle in obstacles_hit:
                return check_obstacle[:2]
            obstacles_hit.add(check_obstacle)

            guard_location = (end_spot, guard_location[1])

        elif direction == Direction.WEST:
            obstacle_location = find_west_obstacle(guard_location, new_obstacle_rows)
            end_spot = obstacle_location - horizontal_offset[direction]

            if obstacle_location == -1:
                return False

            check_obstacle = (guard_location[0], obstacle_location, direction)
            if check_obstacle in obstacles_hit:
                return check_obstacle[:2]
            obstacles_hit.add(check_obstacle)

            guard_location = (guard_location[0], end_spot)
        elif direction == Direction.EAST:
            obstacle_location = find_east_obstacle(
                guard_location, new_obstacle_rows, total_cols
            )
            end_spot = obstacle_location - horizontal_offset[direction]

            if obstacle_location == total_cols:
                return False

            check_obstacle = (guard_location[0], obstacle_location, direction)
            if check_obstacle in obstacles_hit:
                return check_obstacle[:2]
            obstacles_hit.add(check_obstacle)

            guard_location = (guard_location[0], end_spot)

        direction = rotate_guard(direction)


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
        if direction == Direction.NORTH:
            obstacle_location = find_north_obstacle(guard_location, obstacle_cols)
            end_spot = obstacle_location - vertical_offset[direction]
            for i in range(guard_location[0], end_spot, -1):
                guard_pos = (i, guard_location[1])
                check_for_loop_and_add_to_footpath(
                    direction,
                    footpath,
                    guard_pos,
                    new_obstacles,
                    obstacle_cols,
                    obstacle_rows,
                    total_cols,
                    total_rows,
                )

            guard_location = (end_spot, guard_location[1])

            if obstacle_location == -1:
                # we're leaving
                break
        elif direction == Direction.SOUTH:
            obstacle_location = find_south_obstacle(
                guard_location, obstacle_cols, total_rows
            )
            end_spot = obstacle_location - vertical_offset[direction]

            for i in range(guard_location[0], end_spot):
                guard_pos = (i, guard_location[1])
                check_for_loop_and_add_to_footpath(
                    direction,
                    footpath,
                    guard_pos,
                    new_obstacles,
                    obstacle_cols,
                    obstacle_rows,
                    total_cols,
                    total_rows,
                )

            guard_location = (end_spot, guard_location[1])
            if obstacle_location == total_rows:
                # we're leaving
                break
        elif direction == Direction.WEST:
            obstacle_location = find_west_obstacle(guard_location, obstacle_rows)
            end_spot = obstacle_location - horizontal_offset[direction]

            for i in range(guard_location[1], end_spot, -1):
                guard_pos = (guard_location[0], i)
                check_for_loop_and_add_to_footpath(
                    direction,
                    footpath,
                    guard_pos,
                    new_obstacles,
                    obstacle_cols,
                    obstacle_rows,
                    total_cols,
                    total_rows,
                )

            guard_location = (guard_location[0], end_spot)
            if obstacle_location == -1:
                # we're leaving
                break
        elif direction == Direction.EAST:
            obstacle_location = find_east_obstacle(
                guard_location, obstacle_rows, total_cols
            )
            end_spot = obstacle_location - horizontal_offset[direction]
            for i in range(guard_location[1], end_spot):
                guard_pos = (guard_location[0], i)
                check_for_loop_and_add_to_footpath(
                    direction,
                    footpath,
                    guard_pos,
                    new_obstacles,
                    obstacle_cols,
                    obstacle_rows,
                    total_cols,
                    total_rows,
                )

            guard_location = (guard_location[0], end_spot)
            if obstacle_location == total_cols:
                # we're leaving
                break
        direction = rotate_guard(direction)

    return {"answer": len(new_obstacles)}


def check_for_loop_and_add_to_footpath(
    direction,
    footpath,
    guard_pos,
    new_obstacles,
    obstacle_cols,
    obstacle_rows,
    total_cols,
    total_rows,
):
    footpath.add(guard_pos)
    new_obstacle_coords = (
        guard_pos[0] + vertical_offset[direction],
        guard_pos[1] + horizontal_offset[direction],
    )
    if new_obstacle_coords not in footpath:
        check_loop(
            direction,
            guard_pos,
            new_obstacles,
            obstacle_cols,
            obstacle_rows,
            total_cols,
            total_rows,
        )


def check_loop(
    direction,
    guard_pos,
    new_obstacles,
    obstacle_cols,
    obstacle_rows,
    total_cols,
    total_rows,
):
    if obstacle := find_obstacle_if_exists(
        guard_pos,
        obstacle_cols,
        obstacle_rows,
        total_cols,
        total_rows,
        direction,
    ):
        new_obstacles.add(obstacle)
