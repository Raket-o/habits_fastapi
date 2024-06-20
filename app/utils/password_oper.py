from passlib.context import CryptContext


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def coder_password(password):
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password, hashed_password):
    return PWD_CONTEXT.verify(plain_password, hashed_password)