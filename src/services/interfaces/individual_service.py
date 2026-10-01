from abc import ABC, abstractmethod
from uuid import UUID

from src.models.entities.individual import IndividualTable
from src.models.entities.transaction import TransactionTable
from src.schemas.create_individual_schema import CreateIndividualSchema


class IndividualServiceInterface(ABC):
    @abstractmethod
    def create_client(
        self,
        client_data: CreateIndividualSchema,
    ) -> IndividualTable: ...

    @abstractmethod
    def get_client(
        self,
        client_id: UUID,
    ) -> IndividualTable | None: ...

    @abstractmethod
    def withdraw(
        self,
        client_id: UUID,
        amount: float,
    ) -> None: ...

    @abstractmethod
    def statement(
        self,
        client_id: UUID,
    ) -> list[TransactionTable]: ...
