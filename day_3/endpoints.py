from fastapi import APIRouter

from aoc_types import TaskInput
import re

day_3_routes = APIRouter()


def extract_mul_values(mul_string: str):
    return re.findall(r"mul\([1-9][0-9]*,[1-9][0-9]*\)", mul_string)


def process_mul_strings(mul_string: str):
    mul_lists = extract_mul_values(mul_string)
    # go through each mul value, take out the numbers and convert to integers
    values_to_multiply = [
        [m for m in map(int, mul.strip("mul()").split(","))] for mul in mul_lists
    ]
    # multiply each list together and add up the values
    total = sum(map(lambda x: x[0] * x[1], values_to_multiply))
    return total


def slice_out_ignored_sequences(mul_string: str):
    # split on don't values
    # if they contain a 'do', cut everything after that and add it to the return string
    # if there is no 'do' then it's don't followed by don't, so everything inbetween is to be cut
    split_on_dont = mul_string.split("don't()")
    to_add = [split_on_dont[0]]
    for i in range(1, len(split_on_dont)):
        a = split_on_dont[i].split("do()")
        if len(a) > 1:
            to_add.append(" ".join(a[1:]))

    return " ".join(to_add)


@day_3_routes.post("/1")
async def task_1(task_input: TaskInput):
    total = process_mul_strings(re.sub("\n", " ", task_input.data))

    return {"answer": total}


@day_3_routes.post("/2")
async def task_2(task_input: TaskInput):
    total = process_mul_strings(slice_out_ignored_sequences(task_input.data))

    return {"answer": total}
