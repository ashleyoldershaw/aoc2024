from typing import Tuple, List

from fastapi import APIRouter

from aoc_types import TaskInput, Coordinates
from utils import Direction, get_next_position

day_15_routes = APIRouter()


def parse_input_data(
    puzzle_input: str,
) -> Tuple[Coordinates, List[Direction], List[List[str]]]:
    raw_puzzle_map, raw_instructions = puzzle_input.split("\n\n")

    char_position = None
    puzzle_lines = raw_puzzle_map.splitlines()
    for i, line in enumerate(puzzle_lines):
        for j, char in enumerate(line.strip()):
            if char == "@":
                char_position = (i, j)

    instruction_mapping = {
        "^": Direction.NORTH,
        "v": Direction.SOUTH,
        ">": Direction.EAST,
        "<": Direction.WEST,
    }

    instructions = [
        instruction_mapping[raw_instruction]
        for raw_instruction in raw_instructions
        if raw_instruction in {"^", "v", "<", ">"}
    ]

    puzzle_map = [list(line) for line in puzzle_lines]
    puzzle_map[char_position[0]][char_position[1]] = "."

    return char_position, instructions, puzzle_map


def parse_converter_input_data(
    puzzle_input: str,
) -> Tuple[Coordinates, List[Direction], List[List[str]]]:
    raw_puzzle_map, raw_instructions = puzzle_input.split("\n\n")

    char_position = None
    puzzle_lines = raw_puzzle_map.splitlines()
    puzzle_map = []
    for i, line in enumerate(puzzle_lines):
        new_line = []
        for j, char in enumerate(line.strip()):
            if char == "#":
                new_line.extend(["#", "#"])
            elif char == "@":
                char_position = (i, j * 2)
                new_line.extend([".", "."])
            elif char == "O":
                new_line.extend(["[", "]"])
            elif char == ".":
                new_line.extend([".", "."])
        puzzle_map.append(new_line)

    instruction_mapping = {
        "^": Direction.NORTH,
        "v": Direction.SOUTH,
        ">": Direction.EAST,
        "<": Direction.WEST,
    }

    instructions = [
        instruction_mapping[raw_instruction]
        for raw_instruction in raw_instructions
        if raw_instruction in {"^", "v", "<", ">"}
    ]

    return char_position, instructions, puzzle_map


def free_space_behind_barrel(
    puzzle_map: List[List[str]], barrel: Coordinates, direction: Direction
) -> Coordinates | None:
    """
    Check behind a barrel for a wall or a free space
    :param puzzle_map: the puzzle map to check
    :param barrel: the location of the initial barrel to check
    :param direction: the direction to look
    :return: None if no free space, a coordinate of free space if there is
    """
    location_to_check = barrel
    while True:
        next_spot = get_next_position(location_to_check, direction)
        if puzzle_map[next_spot[0]][next_spot[1]] == "O":
            # found a barrel, so need to keep going
            location_to_check = next_spot
            continue
        elif puzzle_map[next_spot[0]][next_spot[1]] == "#":
            # found a wall, so no free space
            return None
        else:
            return next_spot


def follow_instructions(task_input: str):
    char_position, instructions, puzzle_map = parse_input_data(task_input)

    while instructions:
        direction = instructions.pop(0)

        next_position = get_next_position(char_position, direction)
        if puzzle_map[next_position[0]][next_position[1]] == "#":
            continue
        elif puzzle_map[next_position[0]][next_position[1]] == ".":
            char_position = next_position
        elif puzzle_map[next_position[0]][next_position[1]] == "O":
            if free_space := free_space_behind_barrel(
                puzzle_map, next_position, direction
            ):
                puzzle_map[next_position[0]][next_position[1]] = "."
                puzzle_map[free_space[0]][free_space[1]] = "O"
                char_position = next_position
            else:
                # No free space found, so can't push barrel or move
                continue
    return puzzle_map


def puzzle_map_string(puzzle_map: List[List[str]]) -> str:
    return "\n".join(["".join(line) for line in puzzle_map])


def calculate_total(puzzle_map: List[List[str]]) -> int:
    total = 0
    for i, line in enumerate(puzzle_map):
        for j, char in enumerate(line):
            if char in ["O", "["]:
                total += i * 100 + j

    return total


def free_space_behind_wide_barrel(
    puzzle_map: List[List[str]], barrel: Coordinates, direction: Direction
) -> Coordinates | None:
    """
    Check behind a wide barrel for a wall or a free space
    This only works when travelling east or west!
    :param puzzle_map: the puzzle map to check
    :param barrel: the location of the initial barrel to check
    :param direction: the direction to look
    :return: None if no free space, a coordinate of free space if there is
    """
    location_to_check = barrel
    while True:
        next_spot = get_next_position(location_to_check, direction)
        if puzzle_map[next_spot[0]][next_spot[1]] in ["[", "]"]:
            # found a barrel, so need to keep going
            location_to_check = next_spot
            continue
        elif puzzle_map[next_spot[0]][next_spot[1]] == "#":
            # found a wall, so no free space
            return None
        else:
            return next_spot


def follow_instructions_part_2(task_input: str):
    char_position, instructions, puzzle_map = parse_converter_input_data(task_input)

    while instructions:
        direction = instructions.pop(0)

        next_position = get_next_position(char_position, direction)
        next_location_char = puzzle_map[next_position[0]][next_position[1]]
        if next_location_char == "#":
            continue
        elif next_location_char == ".":
            puzzle_map[char_position[0]][char_position[1]] = "."
            puzzle_map[next_position[0]][next_position[1]] = "@"
            char_position = next_position
            continue
        else:
            # hit a barrel, and what happens next depends on the direction
            if direction == Direction.EAST or direction == Direction.WEST:
                if free_space := free_space_behind_wide_barrel(
                    puzzle_map, next_position, direction
                ):
                    removed_space = puzzle_map[free_space[0]].pop(free_space[1])
                    puzzle_map[next_position[0]].insert(next_position[1], removed_space)
                    puzzle_map[char_position[0]][char_position[1]] = "."
                    puzzle_map[next_position[0]][next_position[1]] = "@"
                    char_position = next_position
                else:
                    continue
            else:
                # if pushing north or south
                if next_location_char == "[":
                    base = next_position
                else:
                    # next_location_char == ']':
                    base = (next_position[0], next_position[1] - 1)
                to_check = [base, (base[0], base[1] + 1)]
                bases_to_move = [base]
                wall_in_way = False

                while to_check:
                    barrel_position = to_check.pop(0)
                    pos_to_check = get_next_position(barrel_position, direction)
                    next_location_char = puzzle_map[pos_to_check[0]][pos_to_check[1]]

                    if next_location_char == "[":
                        base = pos_to_check
                        bases_to_move.append(base)
                        to_check.extend([base, (base[0], base[1] + 1)])
                    elif next_location_char == "]":
                        base = (pos_to_check[0], pos_to_check[1] - 1)
                        bases_to_move.append(base)
                        to_check.extend([base, (base[0], base[1] + 1)])
                    elif next_location_char == "#":
                        wall_in_way = True
                        break

                if wall_in_way:
                    continue

                for base in bases_to_move[::-1]:
                    new_base_location = get_next_position(base, direction)
                    puzzle_map[new_base_location[0]][new_base_location[1]] = "["
                    puzzle_map[new_base_location[0]][new_base_location[1] + 1] = "]"
                    puzzle_map[base[0]][base[1]] = "."
                    puzzle_map[base[0]][base[1] + 1] = "."

                puzzle_map[char_position[0]][char_position[1]] = "."
                puzzle_map[next_position[0]][next_position[1]] = "@"

                char_position = next_position

    return puzzle_map


@day_15_routes.post("/1")
async def task_1(task_input: TaskInput):
    puzzle_map = follow_instructions(task_input.data)

    total = calculate_total(puzzle_map)

    return {"answer": total}


@day_15_routes.post("/2")
async def task_2(task_input: TaskInput):
    puzzle_map = follow_instructions_part_2(task_input.data)

    total = calculate_total(puzzle_map)

    return {"answer": total}
