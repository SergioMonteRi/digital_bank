from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from src.schemas.create_transaction_schema import CreateTransactionSchema

Client = TypeVar("Client")


class ClientRepositoryInterface(ABC, Generic[Client]):
    @abstractmethod
    def create_client(self, client) -> Client:
        pass

    @abstractmethod
    def get_client(self, client_id: UUID) -> Client | None:
        pass

    @abstractmethod
    def apply_transaction(self, transaction: CreateTransactionSchema) -> None: ...
