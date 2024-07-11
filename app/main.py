"""the main module"""
import uvicorn

from asyncpg.exceptions import InvalidCatalogNameError

from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from app.database.connect import Base, engine, session
from app.database.transactions import create_db
from app.api.auth_api import router as auth_router
from app.api.habits_api import router as habits_router
from app.api.user_api import router as user_router
from app.utils import schedule


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        async with engine.begin() as _:
            pass

    except InvalidCatalogNameError:
        await create_db()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
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
