from abc import ABC, abstractmethod
from uuid import UUID

from src.models.entities.transaction import TransactionTable


class IIndividualStatementController(ABC):
    @abstractmethod
    def get_statement(self, client_id: UUID) -> list[TransactionTable]: ...
