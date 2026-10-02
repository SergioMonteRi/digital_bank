from abc import ABC, abstractmethod
from uuid import UUID


class DepositControllerInterface(ABC):
    @abstractmethod
    def deposit(self, client_id: UUID, amount: float) -> None: ...
