"""module for working with transactions"""
from sqlalchemy import and_, update
from sqlalchemy.future import select

from app.database.connect import engine, session
from app.database.models import Book, User


async def get_list_books_db() -> list[Book]:
    """the function returns a list of books in database"""
    qs = await session.execute(select(Book))
    return qs.all()


async def get_detail_book_db(id_book: int) -> Book:
    """the function returns the details of the book in database"""
    qs = await session.execute(select(Book).where(Book.id == id_book))
    return qs.scalar()


async def add_book_db(obj_add_book) -> Book:
    """the function adds a new book in database"""
    book = Book(**obj_add_book)
    session.add(book)
    await session.commit()
    return book


async def patch_book_db(id_book: int, obj_add_book) -> bool:
    """the function updates the book in database"""
    qs = await session.execute(update(Book).where(Book.id == id_book).values(obj_add_book))
    if qs:
        await session.commit()
        return True


async def delete_book_db(id_book: int) -> None:
    """the function deletes the book in database"""
    book = await session.execute(select(Book).where(Book.id == id_book))
    book = book.scalar()
    if book:
        await session.delete(book)
        await session.commit()


async def check_username_password_db(user) -> None:
    """checking for the existence of a user"""
    user = await session.execute(select(User).where(and_(User.username == str(user.username).lower(), User.password == user.password)))
    return user.scalar()


async def set_token_user(user: User, token: str) -> None:
    user.token = token
    await session.commit()


async def get_user_by_token(token: str) -> User:
    user = await session.execute(select(User).where(User.token == token))
    user = user.scalar()
    return user
