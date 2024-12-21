import math
from typing import Dict, List, Set

from fastapi import APIRouter

from aoc_types import TaskInput, Coordinates
from utils import Direction, get_next_position

day_16_routes = APIRouter()


def rotate_clockwise(direction):
    if direction == Direction.NORTH:
        return Direction.EAST
    if direction == Direction.EAST:
        return Direction.SOUTH
    if direction == Direction.SOUTH:
        return Direction.WEST
    if direction == Direction.WEST:
        return Direction.NORTH


def rotate_anticlockwise(direction):
    if direction == Direction.NORTH:
        return Direction.WEST
    if direction == Direction.EAST:
        return Direction.NORTH
    if direction == Direction.SOUTH:
        return Direction.EAST
    if direction == Direction.WEST:
        return Direction.SOUTH


class LocationCosting:
    """
    A representation of a location on the map, and how much it costs to go there
    """

    def __init__(
        self,
        coordinate: Coordinates,
        direction: Direction,
        cost: int,
        previous_positions: Set[Coordinates],
    ):
        self.coordinate = coordinate
        self.direction = direction
        self.cost = cost
        self.explored = False
        self.previous_positions = previous_positions.copy()
        self.previous_positions.add(self.coordinate)

    def __str__(self):
        return f"{self.coordinate} {self.direction} {self.cost} {self.explored=}"

    def estimated_cost(self, goal):
        # TODO implement a goal function for this to make it closer to an A* algorithm than brute force
        distance = math.sqrt(
            (goal[0] - self.coordinate[0]) ** 2 + (goal[1] - self.coordinate[1]) ** 2
        )
        return self.cost + distance


class PuzzleInfo:
    def __init__(self, goal):
        self.locations: Dict[(Coordinates, Direction), LocationCosting] = {}
        self.goal = goal

    def get_cheapest_location(self):
        return min(
            {
                location
                for location in self.locations
                if self.locations[location].explored is False
            },
            key=lambda location: self.locations[location].cost,
        )

    def add_location(self, location: LocationCosting):
        if (location.coordinate, location.direction) not in self.locations:
            self.locations[(location.coordinate, location.direction)] = location
        elif (
            location.cost
            < self.locations[(location.coordinate, location.direction)].cost
        ):
            self.locations[(location.coordinate, location.direction)] = location
        elif (
            location.cost
            == self.locations[(location.coordinate, location.direction)].cost
        ):
            self.locations[
                (location.coordinate, location.direction)
            ].previous_positions.update(location.previous_positions)


def get_possible_moves(costing: LocationCosting, maze: List[str]):
    """
    Get the possible moves and costs associated with them
    :param costing: the location costing to analyse
    :param maze: the map
    :return: a set of location costings to add to the list
    """
    position_in_front = get_next_position(costing.coordinate, costing.direction)
    moves: List[LocationCosting] = []
    if maze[position_in_front[0]][position_in_front[1]] != "#":
        # can move forwards!
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
                costing.cost + 1000,
                costing.previous_positions,
            ),
            LocationCosting(
                costing.coordinate,
                rotate_anticlockwise(costing.direction),
                costing.cost + 1000,
                costing.previous_positions,
            ),
        )
    )

    return moves


def get_minimum_cost_paths(task_input: TaskInput) -> List[LocationCosting]:
    maze = task_input.data.splitlines()
    start_position = None
    end_position = None
    direction = Direction.EAST
    for i, line in enumerate(maze):
        for j, char in enumerate(line):
            if char == "S":
                start_position = (i, j)
            elif char == "E":
                end_position = (i, j)

    # so represent a set of positions, with costings
    # try any possible move, until we get to the end

    puzzle_info = PuzzleInfo(end_position)
    puzzle_info.locations[(start_position, direction)] = LocationCosting(
        start_position, direction, 0, set()
    )
    final_cost = None
    final_costings = []
    while True:
        location = puzzle_info.get_cheapest_location()
        location_costing = puzzle_info.locations[location]
        location_costing.explored = True
        if final_cost and location_costing.cost > final_cost:
            return final_costings
        if location_costing.coordinate == end_position:
            if not final_cost:
                final_cost = location_costing.cost
            final_costings.append(location_costing)
        moves = get_possible_moves(location_costing, maze)
        for move in moves:
            puzzle_info.add_location(move)

        location_costing.explored = True


@day_16_routes.post("/1")
async def task_1(task_input: TaskInput):
    end_locations = get_minimum_cost_paths(task_input)

    return {"answer": end_locations[0].cost}


@day_16_routes.post("/2")
async def task_2(task_input: TaskInput):
    end_locations = get_minimum_cost_paths(task_input)

    locations_on_paths = set()

    for location in end_locations:
        locations_on_paths.update(location.previous_positions)

    return {"answer": len(locations_on_paths)}
