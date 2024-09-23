from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.api import router as api_router

from src.core.config import settings
from src.core.models import db_helper, Base


async def create_tables():
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print("=========================== STAR APPLICATION ===========================")
    yield
    # shutdown
    await db_helper.dispose()
    print("============================ DISPOSE ENGINE ============================")


main_app = FastAPI(
    title="Finance-accounting",
    lifespan=lifespan,
)
main_app.include_router(api_router)

main_app.mount("/media", StaticFiles(directory=settings.media_dir), name="media")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
