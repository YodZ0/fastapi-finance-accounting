from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from core.config import settings
from core.models.database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print('App started...')
    yield
    # shutdown
    print('Dispose engine...')
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router)

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

if __name__ == '__main__':
    uvicorn.run(
        app='main:main_app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
