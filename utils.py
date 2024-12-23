from enum import Enum
from pathlib import Path

from aoc_types import Coordinates, TaskInput


def read_file(file_name: Path):
    """
    Return the contents of a file

    :param file_name:
    :return file contents:
    """
    with open(str(file_name), "r") as f:
        return f.read().strip()


class Direction(Enum):
    """
    Representations of the 4 cardinal directions
    """

    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


vertical_offset = {
    Direction.NORTH: -1,
    Direction.EAST: 0,
    Direction.SOUTH: 1,
    Direction.WEST: 0,
}
horizontal_offset = {
    Direction.NORTH: 0,
    Direction.EAST: 1,
    Direction.SOUTH: 0,
    Direction.WEST: -1,
}


def get_next_position(
    current_position: Coordinates, direction: Direction
) -> Coordinates:
    """
    Get the location of the a positions next step in a direction
    :param current_position: current position of the guard
    :param direction: the direction to look in
    :return: the next step in the specified direction
    """
    return (
        current_position[0] + vertical_offset[direction],
        current_position[1] + horizontal_offset[direction],
    )


class TaskInputWithMapDimensions(TaskInput):
    rows: int
    cols: int
