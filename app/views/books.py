"""books routs processing module"""
from typing import Any

from fastapi import APIRouter, Request

from app.database.models import Book
from app.database.transactions import (
    get_list_books_db,
    get_detail_book_db,
    add_book_db, delete_book_db,
    patch_book_db
)
from app.schemas import books

router = APIRouter(prefix="/books", tags=["books"])


@router.get(
    path="/",
    response_description="books.Listbook",
    response_model=books.ListBooks,
    response_model_exclude_unset=True,
    status_code=200,
)
async def get_list_books(request: Request
                         ) -> dict[str, list[Any]]:
    """the function returns a list of books"""
    res = await get_list_books_db()
    return {"books": [book[0].to_json() for book in await get_list_books_db()]}


@router.get(
    path="/<int:id_book>",
    response_description="books.Book",
    response_model=books.Book,
    # response_model_exclude_unset=True,
    status_code=200,
)
async def get_detail_book(request: Request, id_book: int) -> Book:
    """the function returns the details of the book"""
    return await get_detail_book_db(id_book)


@router.post(
    path="/",
    response_description="books.Book",
    response_model=books.Book,
    status_code=201
)
async def add_book(request: Request, data: books.AddBook) -> Book:
    """the function adds a new book"""
    book = await add_book_db(data.model_dump())
    return book.to_json()


@router.delete(path="/", status_code=204)
async def add_book(request: Request, data: books.DeleteBook) -> None:
    """the function deletes the book"""
    await delete_book_db(data.id)


@router.patch(path="/<int:id_book>",
              response_description="books.Book",
              response_model=books.Book,
              status_code=201)
async def patch_book(request: Request, id_book: int, data: books.AddBook) -> dict[Any, Any]:
    """the function updates the book"""
    dict_data = data.model_dump()
    res = await patch_book_db(id_book, dict_data)
    if res:
        return {**{'id': id_book}, **dict_data}
