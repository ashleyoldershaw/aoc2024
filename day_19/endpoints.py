from collections import defaultdict
from typing import Set, List, Tuple

from fastapi import APIRouter

from aoc_types import TaskInput

day_19_routes = APIRouter()


def check_pattern(options, pattern):
    stubs = defaultdict(int)
    stubs[pattern] = 1
    while stubs:
        stub = max(stubs, key=lambda x: len(x))
        if stub == "":
            break

        for option in {o for o in options if len(o) <= len(stub)}:
            if stub.startswith(option):
                new_stub = stub[len(option) :]
                stubs[new_stub] += stubs[stub]

        del stubs[stub]

    return stubs[""]


def prune_options(raw_options: Set[str]) -> Set[str]:
    """
    Remove options from a set that can already be built by using other options in the set
    For example, if 'b' and 'r' are in the set, we don't need 'br' or 'rb'
    :param raw_options: the patterns to analyse
    :return: a subset of the original options, minus the ones that can already be built from other items in the set
    """
    return {
        option
        for option in raw_options
        if not check_pattern(raw_options.difference({option}), option)
    }


def process_input(task_input: TaskInput) -> Tuple[List[str], Set[str]]:
    lines = task_input.data.splitlines()
    options = {option.strip() for option in lines[0].split(",")}
    patterns = lines[2:]
    return patterns, options


@day_19_routes.post("/1")
async def task_1(task_input: TaskInput):
    patterns, raw_options = process_input(task_input)
    options = prune_options(raw_options)
    total = sum(bool(check_pattern(options, pattern)) for pattern in patterns)

    return {"answer": total}


@day_19_routes.post("/2")
def task_2(task_input: TaskInput):
    patterns, options = process_input(task_input)
    total = sum(check_pattern(options, pattern) for pattern in patterns)

    return {"answer": total}
