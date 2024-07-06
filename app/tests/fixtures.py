import asyncio
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.database.connect import Base, engine, session

from .test_user_opers import USER_DATA


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await session.close()
    await engine.dispose()


@pytest.fixture
def fixture_create_user():
    print("Entering !")

    with TestClient(app) as client:
        _ = client.post(
            url="api/users",
            json=USER_DATA,
        )

    yield

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(drop_db())