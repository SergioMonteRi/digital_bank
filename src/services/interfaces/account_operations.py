from abc import ABC, abstractmethod
from uuid import UUID

from src.models.entities.transaction import TransactionTable


class AccountOperationsInterface(ABC):
    @abstractmethod
    def deposit(self, client_id: UUID, amount: float) -> None: ...

    @abstractmethod
    def withdraw(self, client_id: UUID, amount: float) -> None: ...

    @abstractmethod
    def statement(self, client_id: UUID) -> list[TransactionTable]: ...
