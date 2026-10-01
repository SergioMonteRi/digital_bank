from uuid import UUID

from src.controllers.interfaces.withdraw_controller import WithdrawControllerInterface
from src.services.interfaces.account_operations import AccountOperationsInterface


class WithdrawController(WithdrawControllerInterface):
    def __init__(
        self,
        client_service: AccountOperationsInterface,
    ):
        self.client_service = client_service

    def withdraw(self, client_id: UUID, amount: float) -> None:
        self.client_service.withdraw(client_id, amount)
