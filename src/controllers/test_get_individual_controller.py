from uuid import UUID

from .get_individual_controller import GetIndividualController


class TestGetIndividualController:
    def test_get_individual(self, individual_service):
        individual_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        controller = GetIndividualController(individual_service)

        response = controller.get_individual(individual_id)

        individual_service.get_client.assert_called_once_with(individual_id)

        assert response is individual_service.get_client.return_value
