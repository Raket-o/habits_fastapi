"""books routs processing module"""

from fastapi import APIRouter, Depends

from typing import Annotated

from app.database.models import Habit
from app.database.transactions import (
    get_list_habit_by_telegram_id_db,
    create_habit_db,
)
from app.schemas.habits_sch import CreateHabit, ListBooks
from app.schemas.users_sch import InfoUser

from app.utils.depends import get_current_active_user


router = APIRouter(prefix="/habits", tags=["habits"])


@router.get(
    path="/",
    response_description="habits_sch.ListBooks",
    response_model=ListBooks,
    response_model_exclude_unset=True,
    status_code=200
)
async def get_habits(
    current_user: Annotated[InfoUser, Depends(get_current_active_user)],
):
    res = await get_list_habit_by_telegram_id_db(current_user.id)
    return {"habits": [habit[0].to_json() for habit in res]}


@router.post(
    path="/",
    response_description="habits_sch.CreateHabit",
    response_model=CreateHabit,
    status_code=201
)
async def create_habit(current_user: Annotated[InfoUser, Depends(get_current_active_user)], data: CreateHabit) -> Habit:
    """ """
    data = data.model_dump()
    data.update({"user_id": current_user.id})
    habit = await create_habit_db(data)
    return habit.to_json()


# @router.get(
#     path="/",
#     response_description="books.Listbook",
#     response_model=books.ListBooks,
#     response_model_exclude_unset=True,
#     status_code=200,
# )
# async def get_list_books(request: Request
#                          ) -> dict[str, list[Any]]:
#     """the function returns a list of books"""
#     res = await get_list_books_db()
#     return {"books": [book[0].to_json() for book in await get_list_books_db()]}
#
#
# @router.get(
#     path="/<int:id_book>",
#     response_description="books.Book",
#     response_model=books.Book,
#     # response_model_exclude_unset=True,
#     status_code=200,
# )
# async def get_detail_book(request: Request, id_book: int) -> Book:
#     """the function returns the details of the book"""
#     return await get_detail_book_db(id_book)
#
#
# @router.post(
#     path="/",
#     response_description="books.Book",
#     response_model=books.Book,
#     status_code=201
# )
# async def add_book(request: Request, data: books.AddBook) -> Book:
#     """the function adds a new book"""
#     book = await add_book_db(data.model_dump())
#     return book.to_json()
#
#
# @router.delete(path="/", status_code=204)
# async def add_book(request: Request, data: books.DeleteBook) -> None:
#     """the function deletes the book"""
#     await delete_book_db(data.id)
#
#
# @router.patch(path="/<int:id_book>",
#               response_description="books.Book",
#               response_model=books.Book,
#               status_code=201)
# async def patch_book(request: Request, id_book: int, data: books.AddBook) -> dict[Any, Any]:
#     """the function updates the book"""
#     dict_data = data.model_dump()
#     res = await patch_book_db(id_book, dict_data)
#     if res:
#         return {**{'id': id_book}, **dict_data}
