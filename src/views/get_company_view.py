from src.controllers.interfaces.get_company_controller import (
    GetCompanyControllerInterface,
)
from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.schemas.company_response_schema import CompanyResponseSchema

from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class GetCompanyView(ViewInterface):
    def __init__(self, controller: GetCompanyControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if http_request.param is None or "company_id" not in http_request.param:
            raise HttpBadRequestError("Company id is required")

        company_id = http_request.param["company_id"]

        company = self.__controller.get_company(company_id=company_id)

        response_body = CompanyResponseSchema.model_validate(company).model_dump(
            mode="json"
        )

        return HttpResponse(status_code=200, body=response_body)
