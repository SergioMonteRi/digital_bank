from .create_company_controller import CreateCompanyController


class TestCreateCompanyController:
    def test_create_company(self, company_service, company_data):
        controller = CreateCompanyController(company_service)

        response = controller.create_company(company_data)

        company_service.create_client.assert_called_once_with(company_data)

        assert response is company_service.create_client.return_value
