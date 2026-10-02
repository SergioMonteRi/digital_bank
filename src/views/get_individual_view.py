from src.controllers.interfaces.get_individual_controller import (
    GetIndividualControllerInterface,
)
from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.schemas.individual_response_schema import IndividualResponseSchema

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class GetIndividualView(ViewInterface):
    def __init__(self, controller: GetIndividualControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if http_request.param is None or "individual_id" not in http_request.param:
            raise HttpBadRequestError("Individual id is required")

        individual_id = http_request.param["individual_id"]

        individual = self.__controller.get_individual(individual_id=individual_id)

        response_body = IndividualResponseSchema.model_validate(individual).model_dump(
            mode="json"
        )

        return HttpResponse(status_code=200, body=response_body)
