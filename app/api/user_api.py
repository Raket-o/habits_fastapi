"""users routs processing module"""
from fastapi import APIRouter, Depends

from typing import Annotated

from app.database.transactions import (
    create_user_db,
    get_list_habit_by_telegram_id_db,
)
from app.schemas.users_sch import CreateUserSchemas, InfoUserSchemas
from app.utils.depends import get_current_active_user
from app.utils.password_oper import coder_password


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    path="/",
    response_description="users_sch.GetUser",
    response_model=InfoUserSchemas,
    status_code=201
)
async def create_user(data: CreateUserSchemas) -> dict:
    """ """
    data = data.model_dump()
    data["hashed_password"] = coder_password(data["password"])
    data.pop("password")
    user = await create_user_db(data)
    return user.to_json()


@router.get(
    path="/me/",
    response_description="users_sch.GetUser",
    response_model=InfoUserSchemas,
    status_code=200
)
async def read_user_me(
    current_user: Annotated[InfoUserSchemas, Depends(get_current_active_user)],
) -> dict:
    res = await get_list_habit_by_telegram_id_db(current_user.id)
    habits = [habit[0].to_json() for habit in res]

    current_user = current_user.to_json()
    current_user["habits"] = habits
    return current_user
