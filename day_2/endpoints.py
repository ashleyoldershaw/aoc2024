from fastapi import APIRouter

from aoc_types import TaskInput

day_2_routes = APIRouter()


def check_safety_v1(input_list):
    increasing = input_list[0] < input_list[1]
    for i in range(len(input_list) - 1):
        gap = abs(input_list[i] - input_list[i + 1])
        if 1 > gap or gap > 3:
            return 0

        if increasing:
            if input_list[i] >= input_list[i + 1]:
                return 0
        else:
            if input_list[i] <= input_list[i + 1]:
                return 0

    return 1


def check_safety_with_leveller(input_list):
    # get the overall increasing trend! this insulates against the first being the wrong number
    increasing = input_list[0] < input_list[-1]
    for i in range(len(input_list) - 1):
        problem_item = False
        gap = abs(input_list[i] - input_list[i + 1])
        if 1 > gap or gap > 3:
            problem_item = True

        if increasing:
            if input_list[i] >= input_list[i + 1]:
                problem_item = True
        else:
            if input_list[i] <= input_list[i + 1]:
                problem_item = True

        if problem_item:
            # if one of them is wrong, try and see if either of them work
            return check_safety_v1(
                input_list[:i] + input_list[i + 1 :]
            ) or check_safety_v1(input_list[: i + 1] + input_list[i + 2 :])

    return 1


def parse_input_data(task_input):
    return [
        [integer_value for integer_value in map(int, line.split())]
        for line in task_input.data.strip().splitlines()
    ]


@day_2_routes.post("/1")
async def task_1(task_input: TaskInput):
    safe_lines = sum(map(check_safety_v1, parse_input_data(task_input)))

    return {"answer": safe_lines}


@day_2_routes.post("/2")
async def task_2(task_input: TaskInput):
    safe_lines = sum(map(check_safety_with_leveller, parse_input_data(task_input)))

    return {"answer": safe_lines}
