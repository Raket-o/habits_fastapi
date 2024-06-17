"""module for filling data into a database"""
from datetime import datetime

from sqlalchemy.future import select

from app.database.connect import engine, session
from app.database.models import Habit, TrackingHabit, User


async def filling_db() -> None:
    """the function of filling the database with data of this"""
    async with engine.begin() as _:
        res = await session.execute(select(User))
        if not len(res.all()):
            print("*" * 70)

            users = [
                # User(id=1, username="top", hashed_password="pass1", telegram_id=1),
                User(id=1, username="top", password="pass1", telegram_id=1),
                User(id=2, username="money", password="pass2", telegram_id=2),
                User(id=3, username="jonn", password="pass3", telegram_id=3, is_active=False),
            ]
            session.add_all(users)

            habits = [
                Habit(id=1, user_id=1, name_habit="breakfast"),
                Habit(id=2, user_id=2, name_habit="lunch"),
                Habit(id=3, user_id=3, name_habit="dinner"),

            ]
            session.add_all(habits)

            tracking_habits = [
                TrackingHabit(id=1, habit_id=1),
                TrackingHabit(id=2, habit_id=2, count=5),
                TrackingHabit(id=3, habit_id=3, count=10),

            ]
            session.add_all(tracking_habits)

            await session.commit()
