from uuid import UUID

import pytest

from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.models.entities.individual import IndividualTable

from .get_individual_view import GetIndividualView
from .http_types.http_request import HttpRequest


class TestGetIndividualView:
    def test_handle(self, get_individual_controller, individual_body):
        individual_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        get_individual_controller.get_individual.return_value = IndividualTable(
            id=individual_id,
            balance=500,
            **individual_body,
        )

        expected_body = {
            "id": str(individual_id),
            "balance": 500,
            **individual_body,
        }

        view = GetIndividualView(get_individual_controller)

        response = view.handle(HttpRequest(param={"individual_id": individual_id}))

        get_individual_controller.get_individual.assert_called_once_with(
            individual_id=individual_id
        )

        assert response.status_code == 200
        assert response.body == expected_body

    @pytest.mark.parametrize("param", [None, {}])
    def test_handle_without_individual_id(self, get_individual_controller, param):
        view = GetIndividualView(get_individual_controller)

        with pytest.raises(HttpBadRequestError):
            view.handle(HttpRequest(param=param))

        get_individual_controller.get_individual.assert_not_called()
