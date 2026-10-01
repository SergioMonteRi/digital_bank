from uuid import UUID

from src.controllers.interfaces.statement_controller import (
    StatementControllerInterface,
)
from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.schemas.transaction_response_schema import TransactionResponseSchema

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class StatementView(ViewInterface):
    def __init__(self, controller: StatementControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if http_request.param is None or "client_id" not in http_request.param:
            raise HttpBadRequestError("Client id is required")

        try:
            client_id = UUID(str(http_request.param["client_id"]))
        except ValueError as e:
            raise HttpBadRequestError("Invalid client id") from e

        transactions = self.__controller.get_statement(client_id=client_id)

        response_body = {
            "transactions": [
                TransactionResponseSchema.model_validate(transaction).model_dump(
                    mode="json"
                )
                for transaction in transactions
            ]
        }

        return HttpResponse(status_code=200, body=response_body)
