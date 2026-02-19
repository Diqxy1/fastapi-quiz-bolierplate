from http import HTTPStatus

from src.shared.exceptions.base_exception import BaseException


class ForbiddenException(BaseException):

    def __init__(self, message=None):

        message = message or HTTPStatus.FORBIDDEN.phrase

        super().__init__(message=message, status_code=HTTPStatus.FORBIDDEN.value)