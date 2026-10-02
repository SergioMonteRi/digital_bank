from uuid import UUID

from flask import Blueprint, request

from src.helpers.to_flask_response import to_flask_response
from src.main.composer.create_individual_composer import create_individual_composer
from src.main.composer.get_individual_composer import get_individual_composer
from src.main.composer.individual_deposit_composer import (
    individual_deposit_composer,
)
from src.main.composer.individual_statement_composer import (
    individual_statement_composer,
)
from src.main.composer.individual_withdraw_composer import (
    individual_withdraw_composer,
)
from src.views.http_types.http_request import HttpRequest

individual_routes_bp = Blueprint("individual_routes", __name__)


@individual_routes_bp.route("/individuals", methods=["POST"])
def create_individual():
    http_request = HttpRequest(body=request.get_json(silent=True))

    view = create_individual_composer()

    http_response = view.handle(http_request=http_request)

    return to_flask_response(http_response)


@individual_routes_bp.route("/individuals/<uuid:individual_id>", methods=["GET"])
def get_individual(individual_id: UUID):
    param = {"individual_id": individual_id}

    http_request = HttpRequest(param=param)

    view = get_individual_composer()

    http_response = view.handle(http_request=http_request)

    return to_flask_response(http_response)


@individual_routes_bp.route("/individuals/<uuid:client_id>/deposit", methods=["POST"])
def deposit(client_id: UUID):
    http_request = HttpRequest(
        body=request.get_json(silent=True), param={"client_id": client_id}
    )

    http_response = individual_deposit_composer().handle(http_request=http_request)

    return to_flask_response(http_response)


@individual_routes_bp.route("/individuals/<uuid:client_id>/withdraw", methods=["POST"])
def withdraw(client_id: UUID):
    http_request = HttpRequest(
        body=request.get_json(silent=True), param={"client_id": client_id}
    )

    http_response = individual_withdraw_composer().handle(http_request=http_request)

    return to_flask_response(http_response)


@individual_routes_bp.route("/individuals/<uuid:client_id>/statement", methods=["GET"])
def statement(client_id: UUID):
    http_request = HttpRequest(param={"client_id": client_id})

    http_response = individual_statement_composer().handle(http_request=http_request)

    return to_flask_response(http_response)
