from functools import cache

from fastapi import APIRouter

from aoc_types import TaskInput

day_11_routes = APIRouter()


def parse_input(stones: str) -> list[int]:
    return [int(stone) for stone in stones.split(" ")]


@cache
def get_stones_after_blink(stone):
    if stone == 0:
        return [1]

    string_stone_number = str(stone)
    stone_digits = len(string_stone_number)
    if stone_digits % 2 != 0:
        return [stone * 2024]
    stone_1 = int(string_stone_number[: stone_digits // 2])
    return [stone_1, int(string_stone_number[stone_digits // 2 :])]


@cache
def blink(stone, blinks):
    stones = []
    if blinks == 0:
        return 1

    stones.extend(get_stones_after_blink(stone))

    return sum(blink(stone, blinks - 1) for stone in stones)


@day_11_routes.post("/1")
async def task_1(task_input: TaskInput):
    blinks = 25
    stones = parse_input(task_input.data)

    total = sum(blink(stone, blinks) for stone in stones)
    return {"answer": total}


@day_11_routes.post("/2")
async def task_2(task_input: TaskInput):
    blinks = 75
    stones = parse_input(task_input.data)

    total = sum(blink(stone, blinks) for stone in stones)
    return {"answer": total}
