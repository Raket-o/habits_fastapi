"""the main module"""
import uvicorn

from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from app.database.connect import Base, engine, session
from app.utils.filling_data_base import filling_db
from app.api.auth_api import router as auth_router
from app.api.habits_api import router as habits_router
from app.api.user_api import router as user_router


from config_data.config import DB_TESTS
# from app.database.transactions import create_db
# from app.utils.send_message_tg import send_message_tg


@asynccontextmanager
async def lifespan(app: FastAPI):
    from asyncpg.exceptions import InvalidCatalogNameError
    # await send_message_tg()
    from app.database.transactions import create_db

    try:
        async with engine.begin() as conn:
            pass

    except InvalidCatalogNameError:
        await create_db()


    # if DB_TESTS:
    #     async with engine.begin() as conn:
    #         # await conn.run_sync(Base.metadata.drop_all)
    #         await conn.run_sync(Base.metadata.create_all)
    # else:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from app.utils.schedule import schedule
    # await schedule()

    # from app.database.transactions import remove_old_habits_db
    # await remove_old_habits_db()

    yield

    # if DB_TESTS:
    #     await conn.run_sync(Base.metadata.drop_all)

    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix='/api')
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(habits_router)

app.include_router(api_router)


if __name__ == "__main__":
    # uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    uvicorn.run("main:app", reload=True)
