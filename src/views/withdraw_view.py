from pydantic import ValidationError

from src.controllers.interfaces.withdraw_controller import WithdrawControllerInterface
from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.exceptions.http.http_unprocessable_entity import HttpUnprocessableEntityError
from src.schemas.amount_schema import AmountSchema

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class WithdrawView(ViewInterface):
    def __init__(self, controller: WithdrawControllerInterface):
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if http_request.param is None or "client_id" not in http_request.param:
            raise HttpBadRequestError("Client id is required")

        if http_request.body is None:
            raise HttpBadRequestError("Request body is required")

        client_id = http_request.param["client_id"]

        try:
            withdraw_data = AmountSchema.model_validate(http_request.body)
        except ValidationError as e:
            errors = e.errors(include_url=False, include_context=False)

            raise HttpUnprocessableEntityError(
                message="Invalid request body", errors=errors
            ) from e

        self.__controller.withdraw(client_id, withdraw_data.amount)

        return HttpResponse(status_code=204, body=None)
