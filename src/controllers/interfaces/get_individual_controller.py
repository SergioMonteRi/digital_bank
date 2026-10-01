from abc import ABC, abstractmethod
from uuid import UUID

from src.models.entities.individual import IndividualTable


class IGetIndividualController(ABC):
    @abstractmethod
    def get_individual(self, individual_id: UUID) -> IndividualTable | None: ...
