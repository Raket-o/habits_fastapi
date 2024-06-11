from fastapi import APIRouter,  HTTPException, Request

from fastapi.security import OAuth2PasswordBearer

from app.database.transactions import check_username_password_db, set_token_user, get_user_by_token
from app.schemas.users import User
from app.schemas.token import Token
from app.utils.token import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scopes={})


@router.post(
    path="/login",
    response_description = "Token",
    response_model = Token,
    status_code = 201,
)
async def login(user: User):
    check_user = await check_username_password_db(user)
    if check_user:
        access_token = create_access_token(data={"sub": user.username, "role": "admin"})
        await set_token_user(check_user, access_token)
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get(
    path='/protected',
    status_code = 200
)
async def protected(request: Request):
    """Я понимаю, что на проде так делать нельзя, но это всё, смог сделать в поеде"""
    try:
        access_token = request.headers["access_token"]
        user = await get_user_by_token(access_token)
        if user:
            return {"message": f"Welcome {user.username}"}
        else:
            return {"message": "invalid credentials"}
    except KeyError:
        return {"message": "unknown user"}
