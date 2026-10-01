from flask import jsonify

from src.exceptions.http.http_error import HttpError


def handle_http_error(error: HttpError):
    response = {
        "error": error.name,
        "message": error.message,
    }

    if hasattr(error, "errors"):
        response["errors"] = error.errors

    return jsonify(response), error.status_code
