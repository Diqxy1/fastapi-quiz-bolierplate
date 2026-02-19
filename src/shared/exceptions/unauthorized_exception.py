from http import HTTPStatus

from src.shared.exceptions.base_exception import BaseException


class UnauthorizedException(BaseException):

    def __init__(self, message=None):

        message = message or HTTPStatus.UNAUTHORIZED.phrase

        super().__init__(message=message, status_code=HTTPStatus.UNAUTHORIZED.value)