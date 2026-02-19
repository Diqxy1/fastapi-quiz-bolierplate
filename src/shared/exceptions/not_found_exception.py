from http import HTTPStatus

from src.shared.exceptions.base_exception import BaseException


class NotFoundException(BaseException):

    def __init__(self, message=None):

        message = message or HTTPStatus.NOT_FOUND.phrase

        super().__init__(message=message, status_code=HTTPStatus.NOT_FOUND.value)