from .create_individual_controller import CreateIndividualController


class TestCreateIndividualController:
    def test_create_individual(self, individual_service, individual_data):
        controller = CreateIndividualController(individual_service)

        response = controller.create_individual(individual_data)

        individual_service.create_client.assert_called_once_with(individual_data)

        assert response is individual_service.create_client.return_value
