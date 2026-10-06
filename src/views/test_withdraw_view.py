from decimal import Decimal
from uuid import UUID

import pytest

from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.exceptions.http.http_unprocessable_entity import HttpUnprocessableEntityError

from .http_types.http_request import HttpRequest
from .withdraw_view import WithdrawView


class TestWithdrawView:
    def test_handle(self, withdraw_controller):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")
        amount = Decimal("1000.50")

        view = WithdrawView(withdraw_controller)

        response = view.handle(
            HttpRequest(param={"client_id": client_id}, body={"amount": 1000.50})
        )

        withdraw_controller.withdraw.assert_called_once_with(client_id, amount)

        assert response.status_code == 204
        assert response.body is None

    @pytest.mark.parametrize("param", [None, {}])
    def test_handle_without_client_id(self, withdraw_controller, param):
        view = WithdrawView(withdraw_controller)

        with pytest.raises(HttpBadRequestError):
            view.handle(HttpRequest(param=param, body={"amount": 1000}))

        withdraw_controller.withdraw.assert_not_called()

    def test_handle_without_body(self, withdraw_controller):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        view = WithdrawView(withdraw_controller)

        with pytest.raises(HttpBadRequestError):
            view.handle(HttpRequest(param={"client_id": client_id}, body=None))

        withdraw_controller.withdraw.assert_not_called()

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
    def test_handle_invalid_amount(self, withdraw_controller, body):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        view = WithdrawView(withdraw_controller)

        with pytest.raises(HttpUnprocessableEntityError) as exc_info:
            view.handle(HttpRequest(param={"client_id": client_id}, body=body))

        invalid_fields = {error["loc"][0] for error in exc_info.value.errors}

        assert invalid_fields == {"amount"}

        withdraw_controller.withdraw.assert_not_called()
