from collections import defaultdict
from typing import List, Tuple

from fastapi import APIRouter

from aoc_types import TaskInput, Coordinates
from utils import Direction, get_next_position

day_20_routes: APIRouter = APIRouter()


class Task20Input(TaskInput):
    cutoff: int


def process_input(text_input: str) -> Tuple[Coordinates, Coordinates, List[str]]:
    """
    Get start and end positions of the race, and a map we can easily iterate through
    :param text_input:
    :return:
    """
    race_map = text_input.splitlines()
    start_position = None
    end_position = None
    for i, row in enumerate(race_map):
        for j, col in enumerate(row):
            if col == "S":
                start_position = (i, j)
            elif col == "E":
                end_position = (i, j)
            if start_position and end_position:
                return start_position, end_position, race_map


def find_next_position(escape_map, position, positions):
    for direction in Direction:
        next_pos = get_next_position(position, direction)
        next_position_type = escape_map[next_pos[0]][next_pos[1]]
        if next_pos not in positions and next_position_type in [".", "E"]:
            positions[next_pos] = positions[position] + 1
            return next_pos


def solve_map(escape_map, start_location: Coordinates, goal_location: Coordinates):
    position = start_location
    positions = {start_location: 0}
    while True:
        position = find_next_position(escape_map, position, positions)
        if position == goal_location:
            return positions


def get_cheat_positions(position, skips):
    for distance in range(2, skips + 1):
        for offset in range(distance + 1):
            y_offset = offset
            x_offset = distance - offset

            yield (position[0] + y_offset, position[1] + x_offset), distance
            if y_offset != 0:
                yield (position[0] - y_offset, position[1] + x_offset), distance
            if x_offset != 0:
                yield (position[0] + y_offset, position[1] - x_offset), distance
            if y_offset != 0 and x_offset != 0:
                yield (position[0] - y_offset, position[1] - x_offset), distance


def find_skip_cheats(route, max_skips):
    cheats = defaultdict(int)
    for position in route:
        for skip, distance in get_cheat_positions(position, max_skips):
            if skip in route:
                original_cost = route[position]
                cost_after_cheat = route[skip]
                difference = cost_after_cheat - original_cost - distance
                if difference > 0:
                    cheats[difference] += 1
    return cheats


@day_20_routes.post("/1")
async def task_1(task_input: Task20Input):
    start_position, end_position, race_map = process_input(task_input.data)

    route = solve_map(race_map, start_position, end_position)
    cheats = find_skip_cheats(route, 2)

    total = sum(
        cheats[cheat_cost] for cheat_cost in cheats if cheat_cost >= task_input.cutoff
    )
    return {"answer": total}


@day_20_routes.post("/2")
def task_2(task_input: Task20Input):
    start_position, end_position, race_map = process_input(task_input.data)

    route = solve_map(race_map, start_position, end_position)
    cheats = find_skip_cheats(route, 20)
    total = sum(
        cheats[cheat_cost] for cheat_cost in cheats if cheat_cost >= task_input.cutoff
    )
    return {"answer": total}
