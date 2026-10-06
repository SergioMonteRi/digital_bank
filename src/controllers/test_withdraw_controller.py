from decimal import Decimal
from uuid import UUID

from .withdraw_controller import WithdrawController


class TestWithdrawController:
    def test_withdraw(self, client_service):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")
        amount = Decimal("1000.00")

        controller = WithdrawController(client_service)

        controller.withdraw(client_id, amount)

        client_service.withdraw.assert_called_once_with(client_id, amount)
