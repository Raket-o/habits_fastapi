"""module for working with transactions"""
import asyncpg

from sqlalchemy import and_, update
from sqlalchemy.future import select

from app.database.connect import engine, session

from config_data.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_TESTS, DB_USER
from app.database.models import User


async def create_db() -> None:
    """database creation function"""
    db_name = "habits_tests" if DB_TESTS else DB_NAME
    cursor = await asyncpg.connect(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    )
    await cursor.execute(f"CREATE DATABASE {db_name};")


# async def get_list_books_db() -> list[Book]:
#     """the function returns a list of books in database"""
#     qs = await session.execute(select(Book))
#     return qs.all()
#
#
async def get_user_by_telegram_id_db(telegram_id: int) -> User:
    """ """
    qs = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return qs.scalar()


async def get_user_by_username(username: str) -> User:
    """ """
    qs = await session.execute(select(User).where(User.username == username))
    return qs.scalar()


async def create_user_db(dict_add_user) -> User:
    """the function adds a new book in database"""
    user = User(**dict_add_user)
    session.add(user)
    await session.commit()
    return user


# async def check_user_is_active_db(telegram_id: int) -> User:
#     """the function adds a new book in database"""
#     qs = await session.execute(select(User).where(User.telegram_id == telegram_id))
#     return qs.scalar()
#
#
# async def patch_book_db(id_book: int, obj_add_book) -> bool:
#     """the function updates the book in database"""
#     qs = await session.execute(update(Book).where(Book.id == id_book).values(obj_add_book))
#     if qs:
#         await session.commit()
#         return True
#
#
# async def delete_book_db(id_book: int) -> None:
#     """the function deletes the book in database"""
#     book = await session.execute(select(Book).where(Book.id == id_book))
#     book = book.scalar()
#     if book:
#         await session.delete(book)
#         await session.commit()
#
#
# async def check_username_password_db(user) -> None:
#     """checking for the existence of a user"""
#     user = await session.execute(select(User).where(and_(User.username == str(user.username).lower(), User.password == user.password)))
#     return user.scalar()
#
#
# async def set_token_user(user: User, token: str) -> None:
#     user.token = token
#     await session.commit()
#
#
# async def get_user_by_token(token: str) -> User:
#     user = await session.execute(select(User).where(User.token == token))
#     user = user.scalar()
#     return user
