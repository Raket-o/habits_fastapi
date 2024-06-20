from datetime import time
from typing import List
from pydantic import BaseModel


class HabitSchemas(BaseModel):
    id: int
    name_habit: str
    description: str
    alert_time: time
    count: int


class ListBooksSchemas(BaseModel):
    """Validate request data"""
    habits: List[HabitSchemas]


class CreateHabitSchemas(BaseModel):
    name_habit: str
    description: str
    alert_time: time


class DeleteHabitSchemas(BaseModel):
    id: int


class PatchHabitSchemas(CreateHabitSchemas):
    pass

