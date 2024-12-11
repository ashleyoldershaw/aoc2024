from fastapi import APIRouter

from aoc_types import TaskInput

day_7_routes = APIRouter()


def check_for_deconcatenation(before, after):
    """
    Check to see if it's possible to remove the number
    :param before: the number to check
    :param after: the number we want to remove
    :return: whether or not we can remove
    """
    after_string = str(after)
    return str(before)[-len(after_string) :] == after_string


def deconcatenate_numbers(before, after):
    """
    Remove number from end of string
    :param before: the number to remove from
    :param after: the number to remove
    :return: what's left over
    """
    return int(str(before)[: -len(str(after))] or "0")


def find_subtree(start, target, numbers, i, allow_concat):
    if i == len(numbers) - 1:
        return start == target
    if start < target:
        return False

    if find_subtree(start - numbers[i], target, numbers, i + 1, allow_concat):
        return True

    if (start / numbers[i]).is_integer() and find_subtree(
        start // numbers[i], target, numbers, i + 1, allow_concat
    ):
        return True

    if (
        allow_concat
        and check_for_deconcatenation(start, numbers[i])
        and find_subtree(
            deconcatenate_numbers(start, numbers[i]),
            target,
            numbers,
            i + 1,
            allow_concat,
        )
    ):
        return True

    return False


def backwards_solution(task_input: TaskInput, allow_concat):
    """
    Start from the back, this way we can prune a hell of a lot of stuff
    For example, if we don't get an integer if we devide, then we wouldn't be able to multiply
    :param task_input:
    :param allow_concat:
    :return:
    """
    total = 0
    puzzles = task_input.data.splitlines()
    for puzzle in puzzles:
        raw_target, raw_numbers = puzzle.split(":")
        start_number = int(raw_target.strip())
        numbers = [int(n) for n in raw_numbers.strip().split(" ")[::-1]]
        target = numbers[-1]

        solution_found = find_subtree(start_number, target, numbers, 0, allow_concat)

        if solution_found:
            total += start_number
    return total


@day_7_routes.post("/1")
async def task_1(task_input: TaskInput):
    total = backwards_solution(task_input, False)
    return {"answer": total}


@day_7_routes.post("/2")
async def task_2(task_input: TaskInput):
    total = backwards_solution(task_input, True)
    return {"answer": total}
