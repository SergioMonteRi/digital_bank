from pydantic import ValidationError

from src.controllers.interfaces.create_individual_controller import (
    CreateIndividualControllerInterface,
)
from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.exceptions.http.http_unprocessable_entity import HttpUnprocessableEntityError
from src.schemas.create_individual_schema import CreateIndividualSchema
from src.schemas.individual_response_schema import IndividualResponseSchema

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class CreateIndividualView(ViewInterface):
    def __init__(self, controller: CreateIndividualControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if http_request.body is None:
            raise HttpBadRequestError("Request body is required")

        try:
            individual_data = CreateIndividualSchema.model_validate(http_request.body)
        except ValidationError as e:
            errors = e.errors(include_url=False, include_context=False)

            raise HttpUnprocessableEntityError(
                message="Invalid request body", errors=errors
            ) from e

        individual = self.__controller.create_individual(
            individual_data=individual_data
        )

        response_body = IndividualResponseSchema.model_validate(individual).model_dump(
            mode="json"
        )

        return HttpResponse(status_code=201, body=response_body)
