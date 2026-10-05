from uuid import UUID

from .get_company_controller import GetCompanyController


class TestGetCompanyController:
    def test_get_company(self, company_service):
        company_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        controller = GetCompanyController(company_service)

        response = controller.get_company(company_id)

        company_service.get_client.assert_called_once_with(company_id)

        assert response is company_service.get_client.return_value
