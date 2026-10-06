from decimal import Decimal
from uuid import UUID

import pytest

from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.models.entities.company import CompanyTable

from .get_company_view import GetCompanyView
from .http_types.http_request import HttpRequest


class TestGetCompanyView:
    def test_handle(self, get_company_controller, company_body):
        company_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        get_company_controller.get_company.return_value = CompanyTable(
            **{**company_body, "monthly_revenue": Decimal("100000.00")},
            id=company_id,
            balance=Decimal("5000.00"),
        )

        expected_body = {
            **company_body,
            "id": str(company_id),
            "monthly_revenue": "100000.00",
            "balance": "5000.00",
        }

        view = GetCompanyView(get_company_controller)

        response = view.handle(HttpRequest(param={"company_id": company_id}))

        get_company_controller.get_company.assert_called_once_with(
            company_id=company_id
        )

        assert response.status_code == 200
        assert response.body == expected_body

    @pytest.mark.parametrize("param", [None, {}])
    def test_handle_without_company_id(self, get_company_controller, param):
        view = GetCompanyView(get_company_controller)

        with pytest.raises(HttpBadRequestError):
            view.handle(HttpRequest(param=param))

        get_company_controller.get_company.assert_not_called()
