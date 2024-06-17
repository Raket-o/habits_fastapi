"""books routs processing module"""
from typing import Any, Dict

from fastapi import APIRouter, Depends, Request
from typing import Annotated

from app.database.models import User
from app.database.transactions import (
    get_user_by_telegram_id_db,
    create_user_db,
)
from app.schemas.users_sch import CreateUser, GetUser
from app.schemas.token_sch import Token


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="/<int:telegram_id>",
    response_description="users.GetUser",
    response_model=GetUser,
    response_model_exclude_unset=True,
    status_code=200,
)
# async def get_user_by_telegram_id(_: Request, current_user: Annotated[User, Depends()]) -> User | dict[str, str | int]:
# # async def get_user_by_telegram_id(_: Request, telegram_id: int) -> User | dict[str, str | int]:
#     """ """
#
#
#     # res = await get_user_by_telegram_id_db(telegram_id)
#
#     # if res:
#     #     return res
#     # else:
#     return {
#         "id": 0,
#         "username": "none",
#         "password": "none",
#         "telegram_id": 0,
#         "is_active": "false"
#     }


async def get_user_by_telegram_id(_: Request, telegram_id: int) -> User | dict[str, str | int]:
    """ """
    res = await get_user_by_telegram_id_db(telegram_id)

    if res:
        return res
    else:
        return {
            "id": 0,
            "username": "none",
            "password": "none",
            "telegram_id": 0,
            "is_active": "false"
        }


@router.post(
    path="/",
    response_description="users.GetUser",
    response_model=Token,
    status_code=201
)
async def create_user(_: Request, data: CreateUser) -> dict[str, Any]:
    """ """
    data = data.model_dump()
    """---------------------------------------------------------------------------------"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    data["hashed_password"] = pwd_context.hash(data["password"])
    data.pop("password")
    """---------------------------------------------------------------------------------"""
    user = await create_user_db(data)

    from app.utils.token import create_access_token
    token = create_access_token(data={"telegram_id":data["telegram_id"]})
    print("+="*50, token)
    # return user.to_json()
    return {"access_token": token}



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
