from abc import ABC, abstractmethod
from uuid import UUID

from src.models.entities.individual import IndividualTable
from src.schemas.create_individual_schema import CreateIndividualSchema


class IIndividualRepository(ABC):
    @abstractmethod
    def create_company(self, company: CreateIndividualSchema) -> IndividualTable:
        pass

    @abstractmethod
    def get_company(self, individual_id: UUID) -> IndividualTable | None:
        pass

    @abstractmethod
    def update_balance(self, individual_id: UUID, value: float) -> None:
        pass
