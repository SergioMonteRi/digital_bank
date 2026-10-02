from typing import Any

from flask import jsonify

from src.exceptions.http.http_error import HttpError


def handle_http_error(error: HttpError):
    response: dict[str, Any] = {
        "error": error.name,
        "message": error.message,
    }

    errors = getattr(error, "errors", None)

    if errors:
        response["errors"] = errors

    return jsonify(response), error.status_code
