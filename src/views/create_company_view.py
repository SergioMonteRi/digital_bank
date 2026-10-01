from pydantic import ValidationError

from src.controllers.interfaces.create_company_controller import (
    CreateCompanyControllerInterface,
)
from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.exceptions.http.http_unprocessable_entity import HttpUnprocessableEntityError
from src.schemas.company_response_schema import CompanyResponseSchema
from src.schemas.create_company_schema import CreateCompanySchema

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class CreateCompanyView(ViewInterface):
    def __init__(self, controller: CreateCompanyControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if http_request.body is None:
            raise HttpBadRequestError("Request body is required")

        try:
            company_data = CreateCompanySchema.model_validate(http_request.body)
        except ValidationError as e:
            errors = e.errors(include_url=False, include_context=False)

            raise HttpUnprocessableEntityError(
                message="Invalid request body", errors=errors
            ) from e

        company = self.__controller.create_company(company_data=company_data)

        response_body = CompanyResponseSchema.model_validate(company).model_dump(
            mode="json"
        )

        return HttpResponse(status_code=201, body=response_body)
