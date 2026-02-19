from http import HTTPStatus

from src.shared.exceptions.base_exception import BaseException


class BadRequestException(BaseException):

    def __init__(self, message=None):

        message = message or HTTPStatus.BAD_REQUEST.phrase

        super().__init__(message=message, status_code=HTTPStatus.BAD_REQUEST.value)