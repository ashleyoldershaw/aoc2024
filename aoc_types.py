from pydantic import BaseModel


class TaskInput(BaseModel):
    data: str
