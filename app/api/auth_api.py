"""auth routs processing module"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database.transactions import get_user_by_username_db
from app.schemas.token_sch import TokenSchemas
from app.utils.password_oper import verify_password
from app.utils.token_oper import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={})


async def authenticate_user(username: str, password: str):
    """the function checks if the user is authenticated"""
    user = await get_user_by_username_db(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenSchemas:
    """the function returns a token if the username and password are correct"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "telegram_id": user.telegram_id}
    )
    return TokenSchemas(access_token=access_token, token_type="bearer")
