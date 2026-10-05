from uuid import UUID

import pytest

from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.exceptions.http.http_unprocessable_entity import HttpUnprocessableEntityError
from src.models.entities.company import CompanyTable
from src.schemas.create_company_schema import CreateCompanySchema

from .create_company_view import CreateCompanyView
from .http_types.http_request import HttpRequest


class TestCreateCompanyView:
    def test_handle(self, create_company_controller, company_body):
        company_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        create_company_controller.create_company.return_value = CompanyTable(
            id=company_id,
            balance=0,
            **company_body,
        )

        expected_body = {
            "id": str(company_id),
            "balance": 0,
            **company_body,
        }

        view = CreateCompanyView(create_company_controller)

        response = view.handle(HttpRequest(body=company_body))

        create_company_controller.create_company.assert_called_once_with(
            company_data=CreateCompanySchema(**company_body)
        )

        assert response.status_code == 201
        assert response.body == expected_body

    def test_handle_without_body(self, create_company_controller):
        view = CreateCompanyView(create_company_controller)

        with pytest.raises(HttpBadRequestError):
            view.handle(HttpRequest(body=None))

        create_company_controller.create_company.assert_not_called()

    def test_handle_invalid_body(self, create_company_controller, company_body):
        del company_body["company_name"]
        company_body["monthly_revenue"] = "not a number"

        view = CreateCompanyView(create_company_controller)

        with pytest.raises(HttpUnprocessableEntityError) as exc_info:
            view.handle(HttpRequest(body=company_body))

        invalid_fields = {error["loc"][0] for error in exc_info.value.errors}

        assert invalid_fields == {"company_name", "monthly_revenue"}

        create_company_controller.create_company.assert_not_called()
