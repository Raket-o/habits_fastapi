"""the main module"""
import uvicorn

from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from app.database.connect import Base, engine, session
from app.utils.filling_data_base import filling_db
from app.views.user import router as user_router

from config_data.config import DB_TESTS
# from app.database.transactions import create_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    if DB_TESTS:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    else:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # await filling_db()

    yield
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix='/api')
api_router.include_router(user_router)

app.include_router(api_router)


if __name__ == "__main__":
    # uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    uvicorn.run("main:app", reload=True)
