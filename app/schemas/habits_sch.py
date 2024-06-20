from typing import List

from pydantic import BaseModel


# class Habit(BaseModel):
#     ...

class Habit(BaseModel):
    id: int
    user_id: int
    name_habit: str
    description: str


class ListBooks(BaseModel):
    """Validate request data"""
    habits: List[Habit]


class CreateHabit(BaseModel):
    # user_id: int
    name_habit: str
    description: str
