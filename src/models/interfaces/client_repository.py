from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

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
