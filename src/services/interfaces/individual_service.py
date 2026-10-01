from abc import abstractmethod
from uuid import UUID

from src.models.entities.individual import IndividualTable
from src.schemas.create_individual_schema import CreateIndividualSchema

from .account_operations import AccountOperationsInterface


class IndividualServiceInterface(AccountOperationsInterface):
    @abstractmethod
    def create_client(
        self,
        client_data: CreateIndividualSchema,
    ) -> IndividualTable: ...

    @abstractmethod
    def get_client(
        self,
        client_id: UUID,
    ) -> IndividualTable: ...
