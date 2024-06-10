"""module for filling data into a database"""
from datetime import datetime

from sqlalchemy.future import select

from app.database.connect import engine, session
from app.database.models import Book, Task, User


async def filling_db() -> None:
    """the function of filling the database with data of this"""
    async with engine.begin() as conn:
        res = await session.execute(select(User))
        if not len(res.all()):
            print("*" * 70)

            books = [
                Book(name="Book1"),
                Book(name="Book2"),
                Book(name="Book3"),
                Book(name="Book4"),
                Book(name="Book5"),
            ]
            session.add_all(books)

            users = [
                User(username="top", password="pass"),
                User(username="money", password="pass"),
                User(username="jonn", password="pass"),
            ]
            session.add_all(users)

            tasks = [
                Task(name="go to shop", created_datetime=datetime.now().replace(day=5, microsecond=0), user_id=1),
                Task(name="go to home", created_datetime=datetime.now().replace(day=10, microsecond=0), user_id=2),
                Task(name="go to ocean", created_datetime=datetime.now().replace(day=15, microsecond=0), user_id=3),
            ]
            session.add_all(tasks)

            await session.commit()
