from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.shared.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException
)


def init_app(app: FastAPI):

    @app.exception_handler(BadRequestException)
    def bad_request_error(request: Request, error: BadRequestException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )

    @app.exception_handler(NotFoundException)
    def not_found_request_error(request: Request, error: NotFoundException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )

    @app.exception_handler(UnauthorizedException)
    def unauthorized_request_error(request: Request, error: UnauthorizedException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )

    @app.exception_handler(ForbiddenException)
    def forbidden_request_error(request: Request, error: ForbiddenException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )