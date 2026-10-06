from decimal import Decimal
from uuid import UUID

from .deposit_controller import DepositController


class TestDepositController:
    def test_deposit(self, client_service):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")
        amount = Decimal("1000.00")

        controller = DepositController(client_service)

        controller.deposit(client_id, amount)

        client_service.deposit.assert_called_once_with(client_id, amount)
