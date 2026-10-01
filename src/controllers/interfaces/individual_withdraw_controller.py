from abc import ABC, abstractmethod
from uuid import UUID


class IIndividualWithdrawController(ABC):
    @abstractmethod
    def withdraw(self, client_id: UUID, amount: float) -> None: ...
