from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from api import router
from core.config import config
from core.exceptions.handler import init_exception_handler
from core.fastapi.middlewares.sqlalchemy import SQLAlchemyMiddleware


def init_routers(app: FastAPI) -> None:
    app.include_router(router)


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SQLAlchemyMiddleware)
    ]
    return middleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="assignment-sehyeongkim",
        version="0.1",
        docs_url=None if config.ENV == "prod" else "/docs",
        redoc_url=None if config.ENV == "prod" else "/redoc",
        middleware=make_middleware()
    )
    init_routers(app=app)
    init_exception_handler(app=app)
    return app

app = create_app()
