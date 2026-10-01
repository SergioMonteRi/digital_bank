from abc import ABC, abstractmethod

from src.models.entities.individual import IndividualTable
from src.schemas.create_individual_schema import CreateIndividualSchema


class CreateIndividualControllerInterface(ABC):
    @abstractmethod
    def create_individual(
        self, individual_data: CreateIndividualSchema
    ) -> IndividualTable: ...
