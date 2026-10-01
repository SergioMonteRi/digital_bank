from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from src.enum.client_type import ClientType
from src.models.entities.transaction import TransactionTable

Client = TypeVar("Client")


class ClientRepositoryInterface(ABC, Generic[Client]):
    @abstractmethod
    def create_client(self, client) -> Client:
        pass

    @abstractmethod
    def get_client(self, client_id: UUID) -> Client | None:
        pass

    @abstractmethod
    def update_balance(self, client_id: UUID, value: float) -> None:
        pass

    @abstractmethod
    def get_statement(
        self, client_id: UUID, client_type: ClientType
    ) -> list[TransactionTable]:
        pass
