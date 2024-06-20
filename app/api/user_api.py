"""users routs processing module"""
from fastapi import APIRouter, Depends

from typing import Annotated

from app.database.models import User
from app.database.transactions import (
    create_user_db,
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
async def create_user(data: CreateUserSchemas) -> User:
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
):
    return current_user
