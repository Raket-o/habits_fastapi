"""the fixture module"""
import asyncio
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.database.connect import Base, engine, session


USER_DATA:dict = {
    "username": "test",
    "password": "test_password",
    "telegram_id": 177
}


async def drop_db() -> None:
    """the function deletes the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await session.close()
    await engine.dispose()


def run_async_drop_db() -> None:
    """the function starts an asynchronous function"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(drop_db())


@pytest.fixture
def fixture_create_user():
    with TestClient(app) as client:
        _ = client.post(
            url="api/users",
            json=USER_DATA,
        )

    yield
    run_async_drop_db()


def register_user() -> None:
    with TestClient(app) as client:
        _ = client.post(
            url="api/users",
            json=USER_DATA,
        )


def login() -> str:
    with TestClient(app) as client:
        user_data = USER_DATA.copy()
        user_data.pop("telegram_id")
        response = client.post(
            url="api/auth/token",
            data=user_data
        )
    return response.json()["access_token"]