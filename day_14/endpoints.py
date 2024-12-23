import re
from typing import Tuple, List

from fastapi import APIRouter

from collections import defaultdict

from utils import TaskInputWithMapDimensions

day_14_routes = APIRouter()


def get_button_vector(line: str) -> Tuple[int, int, int, int]:
    x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
    return x, y, vx, vy


def get_quadrant(position, rows, cols):
    quadrant_height = rows // 2
    quadrant_width = cols // 2

    if position[0] < quadrant_width:
        if position[1] < quadrant_height:
            return "nw"
        if position[1] > rows - 1 - quadrant_height:
            return "sw"

    if position[0] > cols - 1 - quadrant_width:
        if position[1] < quadrant_height:
            return "ne"
        if position[1] > rows - 1 - quadrant_height:
            return "se"

    return "none"


@day_14_routes.post("/1")
async def task_1(task_input: TaskInputWithMapDimensions):
    seconds_passing = 100
    positions = []
    for line in task_input.data.splitlines():
        x, y, vx, vy = get_button_vector(line)

        new_x = (x + seconds_passing * vx) % task_input.cols
        new_y = (y + seconds_passing * vy) % task_input.rows

        positions.append((new_x, new_y))

    counter = defaultdict(int)
    for position in positions:
        quadrant = get_quadrant(position, task_input.rows, task_input.cols)
        counter[quadrant] += 1

    return {"answer": counter["ne"] * counter["se"] * counter["sw"] * counter["nw"]}


class Bot:
    """
    Representation of a robot, can move
    """

    def __init__(self, x: int, y: int, vx: int, vy: int, rows: int, cols: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.rows = rows
        self.cols = cols

    def move(self):
        self.x = (self.x + self.vx) % self.cols
        self.y = (self.y + self.vy) % self.rows

    def __str__(self):
        return f"{self.x}, {self.y}, {self.vx}, {self.vy}"


def print_map(bots: List[Bot], rows: int, cols: int):
    locations = defaultdict(int)
    for bot in bots:
        locations[(bot.x, bot.y)] += 1
    robot_map = [[" " for _ in range(cols)] for _ in range(rows)]

    for location in locations:
        robot_map[location[1]][location[0]] = str(locations[location])

    print("\n".join(["".join(line) for line in robot_map]))


@day_14_routes.post("/2")
async def task_2(task_input: TaskInputWithMapDimensions):
    total = 0
    return {"answer": total}


if __name__ == "__main__":
    with open("test_input.txt", "r") as f:
        test_map = f.read().strip()

    map_lines = test_map.splitlines()
    rows = 103
    cols = 101
    bots = [Bot(*get_button_vector(line), rows, cols) for line in map_lines]

    max_in_middle = 0
    frame_number = 0
    for i in range(10000):
        in_middle = 0
        for bot in bots:
            bot.move()
            if bot.x == 51:
                in_middle += 1
            if bot.y == 52:
                in_middle += 1
        if in_middle > max_in_middle:
            max_in_middle = in_middle
            frame_number = i + 1
            print(f"***FRAME {frame_number}***")
            print_map(bots, rows, cols)

    print(f"Most in middle was frame {frame_number} with {max_in_middle} bots")
