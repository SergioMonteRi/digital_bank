from uuid import UUID

from pydantic import ValidationError

from src.controllers.interfaces.deposit_controller import DepositControllerInterface
from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.exceptions.http.http_unprocessable_entity import HttpUnprocessableEntityError
from src.schemas.amount_schema import AmountSchema

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class DepositView(ViewInterface):
    def __init__(self, controller: DepositControllerInterface):
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if http_request.param is None or "client_id" not in http_request.param:
            raise HttpBadRequestError("Client id is required")

        if http_request.body is None:
            raise HttpBadRequestError("Request body is required")

        try:
            client_id = UUID(str(http_request.param["client_id"]))
        except ValueError as e:
            raise HttpBadRequestError("Invalid client id") from e

        try:
            deposit_data = AmountSchema.model_validate(http_request.body)
        except ValidationError as e:
            errors = e.errors(include_url=False, include_context=False)

            raise HttpUnprocessableEntityError(
                message="Invalid request body", errors=errors
            ) from e

        self.__controller.deposit(client_id, deposit_data.amount)

        return HttpResponse(status_code=204, body=None)
