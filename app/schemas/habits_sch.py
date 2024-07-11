"""the schematics module for answering about the habit"""

from datetime import time
from typing import List, Optional

from pydantic import BaseModel


class HabitSchemas(BaseModel):
    id: int
    habit_name: str
    description: str
    alert_time: time
    count: int


class ListHabitsSchemas(BaseModel):
    habits: List[HabitSchemas]


class CreateHabitSchemas(BaseModel):
    habit_name: str
    description: str
    alert_time: time


class DeleteHabitSchemas(BaseModel):
    id: int


class PatchHabitSchemas(BaseModel):
    habit_name: Optional[str] = None
    description: Optional[str] = None
    alert_time: Optional[time] = None


class FulfilHabitSchemas(BaseModel):
    id: int
