from datetime import time
from typing import List, Optional
from pydantic import BaseModel


class HabitSchemas(BaseModel):
    id: int
    name_habit: str
    description: str
    alert_time: time
    count: int


class ListHabitsSchemas(BaseModel):
    """Validate request data"""
    habits: List[HabitSchemas]


class CreateHabitSchemas(BaseModel):
    name_habit: str
    description: str
    alert_time: time


class DeleteHabitSchemas(BaseModel):
    id: int


class PatchHabitSchemas(BaseModel):
    name_habit: Optional[str] = None
    description: Optional[str] = None
    alert_time: Optional[time] = None


class FulfilHabitSchemas(DeleteHabitSchemas):
    pass
