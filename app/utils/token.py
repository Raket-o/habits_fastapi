import datetime
from jsonwebtoken import encode

from config_data.config import ALGORITHM, SECRET_KEY


# def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
def create_access_token(data: dict, telegram_id: int):
    to_encode = data.copy()
    # if expires_delta:
    #     expire = datetime.datetime.now() + expires_delta
    # else:
    #     expire = datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"telegram_id": telegram_id})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



