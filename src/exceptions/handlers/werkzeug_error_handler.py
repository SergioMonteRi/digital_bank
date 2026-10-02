from flask import jsonify
from werkzeug.exceptions import HTTPException


def handle_werkzeug_error(error: HTTPException):
    return jsonify({"error": error.name, "message": error.description}), error.code
