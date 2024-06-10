"""the main module"""
import uvicorn

from fastapi import FastAPI, APIRouter
# from app.api.auth import router as auth_router
# from app.api.books import router as books_router
from contextlib import asynccontextmanager

from app.database.connect import Base, engine, session
from app.utils.filling_data_base import filling_db
from config_data.config import DB_TESTS



@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    #
    # await filling_db()
    #
    #
    # yield
    # await session.close()
    # await engine.dispose()

    # try:
    #     async with engine.begin() as conn:
    #         pass
    #
    # except InvalidCatalogNameError:
    #     await create_db()
    #
    # finally:

    if DB_TESTS:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    else:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    await filling_db()

    yield
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix='/api')
# api_router.include_router(auth_router)
# api_router.include_router(books_router)

app.include_router(api_router)


if __name__ == "__main__":
    # uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    uvicorn.run("main:app", reload=True)
