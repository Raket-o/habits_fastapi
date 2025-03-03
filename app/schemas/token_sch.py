"""the schematics module for answering about the token"""

from pydantic import BaseModel


class TokenSchemas(BaseModel):
    access_token: str


class TokenDataSchemas(BaseModel):
    username: str | None = None
