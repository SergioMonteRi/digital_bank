from uuid import UUID

from src.controllers.interfaces.individual_statement_controller import (
    IIndividualStatementController,
)
from src.models.entities.transaction import TransactionTable
from src.services.interfaces.individual_service import (
    IndividualServiceInterface,
)


class StatementController(IIndividualStatementController):
    def __init__(
        self,
        individual_service: IndividualServiceInterface,
    ):
        self.__individual_service = individual_service

    def get_statement(
        self,
        client_id: UUID,
    ) -> list[TransactionTable]:
        return self.__individual_service.statement(client_id)
