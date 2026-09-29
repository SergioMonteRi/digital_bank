from abc import ABC, abstractmethod

from src.models.entities.individual import IndividualTable
from src.schemas.create_individual_schema import CreateIndividualSchema


class IIndividualRepository(ABC):
    @abstractmethod
    def create_company(self, company: CreateIndividualSchema) -> IndividualTable:
        pass

    @abstractmethod
    def get_company(self, individual_id: int) -> IndividualTable | None:
        pass

    @abstractmethod
    def update_balance(self, individual_id: int, value: float) -> None:
        pass
