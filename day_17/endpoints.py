import re
from enum import Enum
from functools import cache
from typing import List

from fastapi import APIRouter

from aoc_types import TaskInput

day_17_routes = APIRouter()


@cache
def extract_numbers(line) -> List[int]:
    return list(map(int, re.findall(r"-?\d+", line)))


class OpCode(Enum):
    ADV = "ADV"
    BXL = "BXL"
    BST = "BST"
    JNZ = "JNZ"
    BXC = "BXC"
    OUT = "OUT"
    BDV = "BDV"
    CDV = "CDV"


@cache
def get_opcode(opcode):
    opcode_mapping = {
        0: OpCode.ADV,
        1: OpCode.BXL,
        2: OpCode.BST,
        3: OpCode.JNZ,
        4: OpCode.BXC,
        5: OpCode.OUT,
        6: OpCode.BDV,
        7: OpCode.CDV,
    }
    return opcode_mapping[opcode]


def get_combo_operand(operand, register_a, register_b, register_c):
    if operand <= 3:
        return operand
    if operand == 4:
        return register_a
    if operand == 5:
        return register_b
    if operand == 6:
        return register_c


def check_register_a_value(
    i: int, instructions: List[int], register_b: int, register_c: int
):
    register_a = i
    pointer = 0
    output = []
    match = True
    while pointer < len(instructions) and match:
        opcode = get_opcode(instructions[pointer])
        operand = instructions[pointer + 1]

        combo_operand = get_combo_operand(operand, register_a, register_b, register_c)
        if opcode == OpCode.ADV:
            register_a = register_a // (2**combo_operand)

        elif opcode == OpCode.BXL:
            register_b = register_b ^ operand
        elif opcode == OpCode.BST:
            register_b = combo_operand % 8
        elif opcode == OpCode.JNZ:
            if register_a != 0:
                pointer = operand
                continue
        elif opcode == OpCode.BXC:
            register_b = register_b ^ register_c
        elif opcode == OpCode.OUT:
            output.append(combo_operand % 8)
        elif opcode == OpCode.BDV:
            register_b = register_a // (2**combo_operand)
        elif opcode == OpCode.CDV:
            register_c = register_a // (2**combo_operand)

        pointer += 2
    return output


@day_17_routes.post("/1")
async def task_1(task_input: TaskInput):
    lines = task_input.data.splitlines()
    register_a = extract_numbers(lines[0])[0]
    register_b = extract_numbers(lines[1])[0]
    register_c = extract_numbers(lines[2])[0]

    instructions = extract_numbers(lines[4])

    pointer = 0

    output = []

    while pointer < len(instructions):
        opcode = get_opcode(instructions[pointer])
        operand = instructions[pointer + 1]

        combo_operand = get_combo_operand(operand, register_a, register_b, register_c)
        if opcode == OpCode.ADV:
            register_a = register_a // (2**combo_operand)
        elif opcode == OpCode.BXL:
            register_b = register_b ^ operand
        elif opcode == OpCode.BST:
            register_b = combo_operand % 8
        elif opcode == OpCode.JNZ:
            if register_a != 0:
                pointer = operand
                continue
        elif opcode == OpCode.BXC:
            register_b = register_b ^ register_c
        elif opcode == OpCode.OUT:
            output.append(combo_operand % 8)
        elif opcode == OpCode.BDV:
            register_b = register_a // (2**combo_operand)
        elif opcode == OpCode.CDV:
            register_c = register_a // (2**combo_operand)

        pointer += 2

    answer = ",".join(map(str, output))

    return {"answer": answer}


@day_17_routes.post("/2")
async def task_2(task_input: TaskInput):
    lines = task_input.data.splitlines()
    instructions = extract_numbers(lines[4])

    register_b = extract_numbers(lines[1])[0]
    register_c = extract_numbers(lines[2])[0]
    test_number = 0o100

    while True:
        output = check_register_a_value(
            test_number, instructions, register_b, register_c
        )
        if output == instructions:
            return {"answer": test_number}

        match = all(output[-i] == instructions[-i] for i in range(1, len(output) + 1))
        if match:
            test_number *= 8
        else:
            test_number += 0o1
