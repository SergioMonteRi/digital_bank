from abc import ABC, abstractmethod
from uuid import UUID

from src.enum.client_type import ClientType
from src.models.entities.transaction import TransactionTable


class TransactionRepositoryInterface(ABC):
    @abstractmethod
    def get_statement(
        self,
        client_id: UUID,
        client_type: ClientType,
    ) -> list[TransactionTable]: ...
