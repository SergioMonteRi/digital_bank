from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID


class WithdrawControllerInterface(ABC):
    @abstractmethod
    def withdraw(self, client_id: UUID, amount: Decimal) -> None: ...
