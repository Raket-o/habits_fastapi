from fastapi import APIRouter,  HTTPException, Request, Depends, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Annotated

from datetime import timedelta
from config_data.config import ACCESS_TOKEN_EXPIRE_MINUTES

# from app.database.transactions import check_username_password_db, set_token_user, get_user_by_token
from app.schemas.users_sch import LoginUser
from app.schemas.token_sch import Token
from app.utils.token_oper import create_access_token
from app.utils.password_oper import verify_password

from app.database.transactions import get_user_by_telegram_id_db, get_user_by_username


router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scopes={})


async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# @router.post(
#     path="/login",
#     response_description = "Token",
#     response_model = Token,
#     status_code = 201,
# )
# async def login(user_data: LoginUser):
#     user = await authenticate_user(user_data.username, user_data.password)
#     if user:
#         access_token = create_access_token(data={"sub": user.username, "telegram_id": user.telegram_id})
#         return {"access_token": access_token}
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
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
    return Token(access_token=access_token, token_type="bearer")



# from app.utils.password_oper import verify_password
# async def authenticate_user(telegram_id: int, password: str):
#     user = await get_user_by_telegram_id_db(telegram_id)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# class OAuth2PasswordRequestFormCustom(OAuth2PasswordRequestForm):




# @router.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     user = await authenticate_user(form_data.telegram_id, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     # access_token = create_access_token(
#     #     data={"sub": user.username}, expires_delta=access_token_expires
#     # )
#     access_token = create_access_token(data={"sub": user.username, "telegram_id": user.telegram_id})
#
#     return Token(access_token=access_token, token_type="bearer")


# @router.get(
#     path='/protected',
#     status_code = 200
# )
# async def protected(request: Request):
#     """Я понимаю, что на проде так делать нельзя, но это всё, смог сделать в поеде"""
#     try:
#         access_token = request.headers["access_token"]
#         user = await get_user_by_token(access_token)
#         if user:
#             return {"message": f"Welcome {user.username}"}
#         else:
#             return {"message": "invalid credentials"}
#     except KeyError:
#         return {"message": "unknown user"}
