import logging

from flask import jsonify

logger = logging.getLogger(__name__)


def handle_unexpected_error(error: Exception):
    logger.exception("Unexpected error", exc_info=error)

    return jsonify({"error": "InternalServerError", "message": "Unexpected error"}), 500
