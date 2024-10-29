import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.exceptions.base import CustomException


def init_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        traceback.print_exc()
        return JSONResponse(
            status_code=422,
            content={'error_code': 422, 'message': exc.body}
        )


    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        traceback.print_exc()
        return JSONResponse(
            status_code=exc.code,
            content={'error_code': exc.error_code, 'message': exc.message},
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={'error_code': 500, 'message': 'Unexpected exception happened.'}
        )
