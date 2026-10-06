from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID


class DepositControllerInterface(ABC):
    @abstractmethod
    def deposit(self, client_id: UUID, amount: Decimal) -> None: ...
