"""module for working with transactions"""
import asyncpg

from sqlalchemy import and_, update
from sqlalchemy.future import select

from app.database.connect import engine, session

from config_data.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_TESTS, DB_USER
from app.database.models import Habit, User


async def create_db() -> None:
    """database creation function"""
    db_name = "habits_tests" if DB_TESTS else DB_NAME
    cursor = await asyncpg.connect(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    )
    await cursor.execute(f"CREATE DATABASE {db_name};")


async def get_user_by_telegram_id_db(telegram_id: int) -> User:
    """ """
    qs = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return qs.scalar()


async def get_user_by_username_db(username: str) -> User:
    """ """
    qs = await session.execute(select(User).where(User.username == username))
    return qs.scalar()


async def create_user_db(dict_add_user) -> User:
    """the function adds a new habit in database"""
    user = User(**dict_add_user)
    session.add(user)
    await session.commit()
    return user


async def get_list_habit_by_telegram_id_db(user_id: int) -> User:
    """the function returns a list of habits in database"""
    qs = await session.execute(select(Habit).where(Habit.user_id == user_id).order_by(Habit.user_id))
    return qs.all()


# async def create_habit_db(dict_add_habit: dict, alert_time: time) -> Habit:
async def create_habit_db(dict_data: dict) -> Habit:
    """the function adds a new habit in database"""
    habit = Habit(**dict_data)
    session.add(habit)
    await session.commit()
    return habit


async def delete_habit_db(id_habit: int) -> None:
    """the function deletes the habit in database"""
    habit = await session.execute(select(Habit).where(Habit.id == id_habit))
    habit = habit.scalar()
    if habit:
        await session.delete(habit)
        await session.commit()


async def patch_habit_db(id_habit: int, dict_patch_habit: dict) -> bool:
    """the function updates the habit in database"""
    qs = await session.execute(update(Habit).where(Habit.id == id_habit).values(dict_patch_habit).returning(Habit))
    if qs:
        await session.commit()
        return qs.scalar()
