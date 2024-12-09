from fastapi import APIRouter

from aoc_types import TaskInput

day_9_routes = APIRouter()


def parse_input(raw_system_string):
    raw_system_string += "0"
    chunks = [raw_system_string[x : x + 2] for x in range(0, len(raw_system_string), 2)]

    return [
        {"id": i, "length": int(chunk[0]), "free_space": int(chunk[1])}
        for i, chunk in enumerate(chunks)
    ]


def find_free_block(file_system):
    """
    scans through the files and gets the index of the first file that has free space

    :param file_system:
    :return:
    """
    for i, file in enumerate(file_system):
        if file["free_space"] > 0:
            return i


def sort_file_blocks_method_1(file_system):
    while True:
        free_space_block = find_free_block(file_system)
        if free_space_block == len(file_system) - 1:
            return file_system
        end_block = file_system[-1]
        if file_system[free_space_block]["id"] == end_block["id"]:
            file_system[free_space_block]["length"] += 1
            file_system[free_space_block]["free_space"] -= 1

        else:
            file_system.insert(
                free_space_block + 1,
                {
                    "id": end_block["id"],
                    "length": 1,
                    "free_space": file_system[free_space_block]["free_space"] - 1,
                },
            )
            file_system[free_space_block]["free_space"] = 0

        end_block["length"] -= 1
        if end_block["length"] == 0:
            new_end_block = file_system[-2]
            new_end_block["free_space"] += end_block["free_space"] + 1
            file_system.pop()
        else:
            end_block["free_space"] += 1


def sort_file_blocks_method_2(file_system):
    i = len(file_system) - 1
    while i > 0:
        moved_file = False
        for j in range(i):
            if file_system[j]["free_space"] >= file_system[i]["length"]:
                if j + 1 == i:
                    # moving a file to be in front of the last
                    file_system[j + 1]["free_space"] += file_system[j]["free_space"]
                    file_system[j]["free_space"] = 0
                else:
                    file_to_move = file_system.pop(i)
                    file_system.insert(j + 1, file_to_move)
                    old_free_space = file_system[j]["free_space"]
                    file_system[i]["free_space"] += (
                        file_system[j + 1]["length"] + file_system[j + 1]["free_space"]
                    )
                    file_system[j]["free_space"] = 0
                    file_system[j + 1]["free_space"] = (
                        old_free_space - file_system[j + 1]["length"]
                    )
                moved_file = True
                break
        if not moved_file:
            i -= 1

    return file_system


def get_checksum(file_system):
    total = 0
    index = 0

    for file in file_system:
        for i in range(file["length"]):
            total += (i + index) * file["id"]
        index += file["length"] + file["free_space"]

    return total


@day_9_routes.post("/1")
async def task_1(task_input: TaskInput):
    file_system = parse_input(task_input.data)

    sorted_files = sort_file_blocks_method_1(file_system)

    return {"answer": get_checksum(sorted_files)}


@day_9_routes.post("/2")
async def task_2(task_input: TaskInput):
    file_system = parse_input(task_input.data)

    sorted_files = sort_file_blocks_method_2(file_system)

    return {"answer": get_checksum(sorted_files)}
