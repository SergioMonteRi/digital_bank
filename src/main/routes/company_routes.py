from uuid import UUID

from flask import Blueprint, request

from src.helpers.to_flask_response import to_flask_response
from src.main.composer.company_deposit_composer import company_deposit_composer
from src.main.composer.company_statement_composer import company_statement_composer
from src.main.composer.company_withdraw_composer import company_withdraw_composer
from src.main.composer.create_company_composer import create_company_composer
from src.main.composer.get_company_composer import get_company_composer
from src.views.http_types.http_request import HttpRequest

company_routes_bp = Blueprint("company_routes", __name__)


@company_routes_bp.route("/companies", methods=["POST"])
def create_company():
    http_request = HttpRequest(body=request.get_json(silent=True))

    view = create_company_composer()

    http_response = view.handle(http_request=http_request)

    return to_flask_response(http_response)


@company_routes_bp.route("/companies/<uuid:company_id>", methods=["GET"])
def get_company(company_id: UUID):
    param = {"company_id": company_id}

    http_request = HttpRequest(param=param)

    view = get_company_composer()

    http_response = view.handle(http_request=http_request)

    return to_flask_response(http_response)


@company_routes_bp.route("/companies/<uuid:client_id>/deposit", methods=["POST"])
def deposit(client_id: UUID):
    http_request = HttpRequest(
        body=request.get_json(silent=True), param={"client_id": client_id}
    )

    http_response = company_deposit_composer().handle(http_request=http_request)

    return to_flask_response(http_response)


@company_routes_bp.route("/companies/<uuid:client_id>/withdraw", methods=["POST"])
def withdraw(client_id: UUID):
    http_request = HttpRequest(
        body=request.get_json(silent=True), param={"client_id": client_id}
    )

    http_response = company_withdraw_composer().handle(http_request=http_request)

    return to_flask_response(http_response)


@company_routes_bp.route("/companies/<uuid:client_id>/statement", methods=["GET"])
def statement(client_id: UUID):
    http_request = HttpRequest(param={"client_id": client_id})

    http_response = company_statement_composer().handle(http_request=http_request)

    return to_flask_response(http_response)
