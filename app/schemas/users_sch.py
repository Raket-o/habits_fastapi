"""the schematics module for answering about the user"""
from typing import List

from pydantic import BaseModel

from app.schemas.habits_sch import HabitSchemas


class UserSchemas(BaseModel):
    """Return response data"""
    id: int
    username: str
    hashed_password: str
    telegram_id: int
    is_active: bool


class InfoUserSchemas(BaseModel):
    """Return response data"""
    id: int
    username: str
    telegram_id: int
    is_active: bool
    habits: List[HabitSchemas] = None


class CreateUserSchemas(BaseModel):
    """Return response data"""
    username: str
    password: str
    telegram_id: int


class LoginUserSchemas(BaseModel):
    """Return response data"""
    username: str
    password: str
