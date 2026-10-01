from uuid import UUID

from src.controllers.interfaces.statement_controller import StatementControllerInterface
from src.models.entities.transaction import TransactionTable
from src.services.interfaces.account_operations import AccountOperationsInterface


class StatementController(StatementControllerInterface):
    def __init__(
        self,
        client_service: AccountOperationsInterface,
    ):
        self.__client_service = client_service

    def get_statement(
        self,
        client_id: UUID,
    ) -> list[TransactionTable]:
        return self.__client_service.statement(client_id)
