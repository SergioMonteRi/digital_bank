from decimal import Decimal
from uuid import UUID

import pytest

from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.exceptions.http.http_unprocessable_entity import HttpUnprocessableEntityError

from .deposit_view import DepositView
from .http_types.http_request import HttpRequest


class TestDepositView:
    def test_handle(self, deposit_controller):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")
        amount = Decimal("1000.50")

        view = DepositView(deposit_controller)

        response = view.handle(
            HttpRequest(param={"client_id": client_id}, body={"amount": 1000.50})
        )

        deposit_controller.deposit.assert_called_once_with(client_id, amount)

        assert response.status_code == 204
        assert response.body is None

    @pytest.mark.parametrize("param", [None, {}])
    def test_handle_without_client_id(self, deposit_controller, param):
        view = DepositView(deposit_controller)

        with pytest.raises(HttpBadRequestError):
            view.handle(HttpRequest(param=param, body={"amount": 1000}))

        deposit_controller.deposit.assert_not_called()

    def test_handle_without_body(self, deposit_controller):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        view = DepositView(deposit_controller)

        with pytest.raises(HttpBadRequestError):
            view.handle(HttpRequest(param={"client_id": client_id}, body=None))

        deposit_controller.deposit.assert_not_called()

    @pytest.mark.parametrize(
        "body",
        [
            {},
            {"amount": 0},
            {"amount": -100},
            {"amount": "not a number"},
            {"amount": float("inf")},
            {"amount": 10.555},
        ],
    )
    def test_handle_invalid_amount(self, deposit_controller, body):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        view = DepositView(deposit_controller)

        with pytest.raises(HttpUnprocessableEntityError) as exc_info:
            view.handle(HttpRequest(param={"client_id": client_id}, body=body))

        invalid_fields = {error["loc"][0] for error in exc_info.value.errors}

        assert invalid_fields == {"amount"}

        deposit_controller.deposit.assert_not_called()
