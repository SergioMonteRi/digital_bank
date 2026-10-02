from flask import jsonify

from src.views.http_types.http_response import HttpResponse


def to_flask_response(http_response: HttpResponse):
    if http_response.body is None:
        return "", http_response.status_code

    return jsonify(http_response.body), http_response.status_code
