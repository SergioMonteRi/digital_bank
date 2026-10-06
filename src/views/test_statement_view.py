from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

import pytest

from src.enum.client_type import ClientType
from src.enum.transaction_type import TransactionType
from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.models.entities.transaction import TransactionTable

from .http_types.http_request import HttpRequest
from .statement_view import StatementView


class TestStatementView:
    def test_handle(self, statement_controller):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")
        deposit_id = UUID("01a10d74-0000-7000-8000-000000000001")
        withdraw_id = UUID("01a10d74-0000-7000-8000-000000000002")

        statement_controller.get_statement.return_value = [
            TransactionTable(
                id=deposit_id,
                client_id=client_id,
                client_type=ClientType.COMPANY,
                transaction_type=TransactionType.DEPOSIT,
                amount=Decimal("1000.00"),
                created_at=datetime(2026, 10, 5, 12, 0, tzinfo=timezone.utc),
            ),
            TransactionTable(
                id=withdraw_id,
                client_id=client_id,
                client_type=ClientType.COMPANY,
                transaction_type=TransactionType.WITHDRAW,
                amount=Decimal("300.00"),
                created_at=datetime(2026, 10, 5, 13, 30, tzinfo=timezone.utc),
            ),
        ]

        expected_body = {
            "transactions": [
                {
                    "id": str(deposit_id),
                    "transaction_type": "DEPOSIT",
                    "amount": "1000.00",
                    "created_at": "2026-10-05T12:00:00Z",
                },
                {
                    "id": str(withdraw_id),
                    "transaction_type": "WITHDRAW",
                    "amount": "300.00",
                    "created_at": "2026-10-05T13:30:00Z",
                },
            ]
        }

        view = StatementView(statement_controller)

        response = view.handle(HttpRequest(param={"client_id": client_id}))

        statement_controller.get_statement.assert_called_once_with(client_id=client_id)

        assert response.status_code == 200
        assert response.body == expected_body

    def test_handle_empty_statement(self, statement_controller):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        statement_controller.get_statement.return_value = []

        view = StatementView(statement_controller)

        response = view.handle(HttpRequest(param={"client_id": client_id}))

        assert response.status_code == 200
        assert response.body == {"transactions": []}

    @pytest.mark.parametrize("param", [None, {}])
    def test_handle_without_client_id(self, statement_controller, param):
        view = StatementView(statement_controller)

        with pytest.raises(HttpBadRequestError):
            view.handle(HttpRequest(param=param))

        statement_controller.get_statement.assert_not_called()
