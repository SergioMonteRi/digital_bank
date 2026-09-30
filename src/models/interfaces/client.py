from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

Client = TypeVar("Client")


class ClientInterface(ABC, Generic[Client]):
    @abstractmethod
    def get_client(self, client_id: UUID) -> Client | None: ...

    @abstractmethod
    def withdraw(self, client_id: UUID, amount: float) -> None: ...

    @abstractmethod
    def statement(self, client_id: UUID): ...
