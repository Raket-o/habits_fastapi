"""the schematics module for answering about the user"""
from typing import List

from pydantic import BaseModel

from app.schemas.habits_sch import Habit


class User(BaseModel):
    """Return response data"""
    id: int
    username: str
    hashed_password: str
    telegram_id: int
    is_active: bool


class InfoUser(BaseModel):
    """Return response data"""
    id: int
    username: str
    telegram_id: int
    is_active: bool
    habits: List[Habit] = None


class CreateUser(BaseModel):
    """Return response data"""
    username: str
    password: str
    telegram_id: int


class LoginUser(BaseModel):
    """Return response data"""
    username: str
    password: str
