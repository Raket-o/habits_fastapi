"""module for working with transactions"""

import asyncpg
from config_data.config import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_TESTS,
    DB_USER
)
from sqlalchemy import update
from sqlalchemy.future import select

from app.database.connect import session
from app.database.models import Habit, User


async def create_db() -> None:
    """the function creates a database"""
    db_name = "habits_tests" if DB_TESTS else DB_NAME
    cursor = await asyncpg.connect(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    )
    await cursor.execute(f"CREATE DATABASE {db_name};")


async def get_user_by_telegram_id_db(telegram_id: int) -> User:
    """the function returns the user by telegram id"""
    qs = await session.execute(
        select(User).
        where(User.telegram_id == telegram_id)
    )
    return qs.scalar()


async def get_user_by_username_db(username: str) -> User:
    """the function returns the user by name"""
    qs = await session.execute(select(User).where(User.username == username))
    return qs.scalar()


async def create_user_db(dict_add_user) -> User:
    """the function adds a new user in database"""
    user = User(**dict_add_user)
    session.add(user)
    await session.commit()
    return user


async def get_list_habit_by_telegram_id_db(user_id: int) -> Habit:
    """the function returns a list of habits in database"""
    qs = await session.execute(
        select(Habit).where(Habit.user_id == user_id).order_by(Habit.user_id)
    )
    return qs.all()


async def get_detail_habit_by_telegram_id_db(
        user_id: int,
        habit_id: int
) -> Habit:
    """the function returns a detail of habit in database"""
    qs = await session.execute(
        select(Habit).
        where(Habit.user_id == user_id).
        where(Habit.id == habit_id)
    )
    return qs.one_or_none()


async def create_habit_db(dict_data: dict) -> Habit:
    """the function adds a new habit in database"""
    habit = Habit(**dict_data)
    session.add(habit)
    await session.commit()
    return habit


async def delete_habit_db(user_id: int, habit_id: int) -> None:
    """the function deletes the habit in database"""
    habit = await session.execute(
        select(Habit).
        where(Habit.user_id == user_id).
        where(Habit.id == habit_id)
    )
    habit = habit.scalar()
    if habit:
        await session.delete(habit)
        await session.commit()


async def patch_habit_db(
        user_id: int,
        habit_id: int,
        dict_patch_habit: dict
) -> bool:
    """the function updates the habit in database"""
    dict_patch_habit = {
        k: v for k, v in dict_patch_habit.items() if v is not None
    }
    qs = await session.execute(
        update(Habit)
        .where(Habit.user_id == user_id)
        .where(Habit.id == habit_id)
        .values(dict_patch_habit)
        .returning(Habit)
    )
    if qs:
        await session.commit()
        return qs.scalar()


async def fulfilling_habit_db(user_id: int, habit_id: int) -> Habit:
    """the function fulfilling the habit in database"""
    qs = await session.execute(
        select(Habit).
        where(Habit.user_id == user_id).
        where(Habit.id == habit_id)
    )
    habit = qs.scalar()
    if habit:
        habit.count += 1
        await session.commit()
        return habit


async def remove_old_habits_db() -> None:
    """the function removes old habits in database"""
    qs = await session.execute(select(Habit).where(Habit.count >= 21))
    habits = qs.all()
    if habits:
        for habit in habits:
            await session.delete(habit[0])
        await session.commit()


async def get_habits_by_time_db(region_time) -> list[(Habit, User)]:
    """the function returns the time habit"""
    qs = await session.execute(
        select(Habit, User)
        .join(User, User.id == Habit.user_id)
        .where(Habit.alert_time == region_time)
    )
    habits = qs.all()
    return habits
