from pydantic_core import ErrorDetails

from .http_error import HttpError


class HttpUnprocessableEntityError(HttpError):
    def __init__(self, message: str, errors: list[ErrorDetails] | None) -> None:
        super().__init__(message=message, status_code=422, name="UnprocessableEntity")
        self.errors = errors
