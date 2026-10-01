from abc import ABC, abstractmethod
from uuid import UUID


class WithdrawControllerInterface(ABC):
    @abstractmethod
    def withdraw(self, client_id: UUID, amount: float) -> None: ...
