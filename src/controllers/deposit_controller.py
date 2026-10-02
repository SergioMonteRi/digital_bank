from uuid import UUID

from src.controllers.interfaces.deposit_controller import DepositControllerInterface
from src.services.interfaces.account_operations import AccountOperationsInterface


class DepositController(DepositControllerInterface):
    def __init__(
        self,
        client_service: AccountOperationsInterface,
    ):
        self.__client_service = client_service

    def deposit(self, client_id: UUID, amount: float) -> None:
        self.__client_service.deposit(client_id, amount)
