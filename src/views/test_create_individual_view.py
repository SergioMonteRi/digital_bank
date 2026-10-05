from uuid import UUID

import pytest

from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.exceptions.http.http_unprocessable_entity import HttpUnprocessableEntityError
from src.models.entities.individual import IndividualTable
from src.schemas.create_individual_schema import CreateIndividualSchema

from .create_individual_view import CreateIndividualView
from .http_types.http_request import HttpRequest


class TestCreateIndividualView:
    def test_handle(self, create_individual_controller, individual_body):
        individual_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        create_individual_controller.create_individual.return_value = IndividualTable(
            id=individual_id,
            balance=0,
            **individual_body,
        )

        expected_body = {
            "id": str(individual_id),
            "balance": 0,
            **individual_body,
        }

        view = CreateIndividualView(create_individual_controller)

        response = view.handle(HttpRequest(body=individual_body))

        create_individual_controller.create_individual.assert_called_once_with(
            individual_data=CreateIndividualSchema(**individual_body)
        )

        assert response.status_code == 201
        assert response.body == expected_body

    def test_handle_without_body(self, create_individual_controller):
        view = CreateIndividualView(create_individual_controller)

        with pytest.raises(HttpBadRequestError):
            view.handle(HttpRequest(body=None))

        create_individual_controller.create_individual.assert_not_called()

    def test_handle_invalid_body(self, create_individual_controller, individual_body):
        del individual_body["full_name"]
        individual_body["age"] = "not a number"

        view = CreateIndividualView(create_individual_controller)

        with pytest.raises(HttpUnprocessableEntityError) as exc_info:
            view.handle(HttpRequest(body=individual_body))

        invalid_fields = {error["loc"][0] for error in exc_info.value.errors}

        assert invalid_fields == {"full_name", "age"}

        create_individual_controller.create_individual.assert_not_called()
