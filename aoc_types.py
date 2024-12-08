from typing import Tuple

from pydantic import BaseModel


class TaskInput(BaseModel):
    data: str


# Coordinates in format (row, column)
Coordinates = Tuple[int, int]
