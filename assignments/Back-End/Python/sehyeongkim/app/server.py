from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import router
from core.config import config
from core.exceptions.base import CustomException
from core.exceptions.handler import init_exception_handler
from core.fastapi.middlewares.sqlalchemy import SQLAlchemyMiddleware
from core.fastapi.middlewares.authentication import AuthenticationMiddleware, AuthBackend


def init_routers(app: FastAPI) -> None:
    app.include_router(router)

def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )

def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
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
