from abc import ABC, abstractmethod
from uuid import UUID

from src.models.entities.company import CompanyTable
from src.models.entities.transaction import TransactionTable
from src.schemas.create_company_schema import CreateCompanySchema


class CompanyServiceInterface(ABC):
    @abstractmethod
    def create_client(
        self,
        client_data: CreateCompanySchema,
    ) -> CompanyTable: ...

    @abstractmethod
    def get_client(
        self,
        client_id: UUID,
    ) -> CompanyTable | None: ...

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
