"""dependency module"""

from typing import Annotated

import jwt

from app.database.models import User
from config_data.config import ALGORITHM, SECRET_KEY
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError

from app.database.transactions import get_user_by_username_db
from app.schemas.token_sch import TokenDataSchemas
from app.schemas.users_sch import InfoUserSchemas


async def get_current_user(token: str) -> User:
    """the function returns the current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchemas(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_username_db(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[InfoUserSchemas, Depends(get_current_user)],
) -> InfoUserSchemas:
    """the function of checking whether the user is active"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
