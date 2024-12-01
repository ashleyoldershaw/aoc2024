from fastapi import APIRouter

from aoc_types import TaskInput

day_1_routes = APIRouter()


@day_1_routes.post("/1")
async def day_1_task_1(task_input: TaskInput):
    list_1, list_2 = zip(
        *[map(int, line.split()) for line in task_input.data.strip().splitlines()]
    )
    distance = sum(abs(z[0] - z[1]) for z in zip(*[sorted(list_1), sorted(list_2)]))

    return {"answer": distance}


@day_1_routes.post("/2")
async def day_1_task_2(task_input: TaskInput):
    list_1, list_2 = zip(
        *[map(int, line.split()) for line in task_input.data.strip().splitlines()]
    )
    similarity = 0
    for item in list_1:
        similarity += list_2.count(item) * item
    return {"answer": similarity}
