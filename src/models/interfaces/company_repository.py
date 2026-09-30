from abc import ABC, abstractmethod
from uuid import UUID

from src.enum.client_type import ClientType
from src.models.entities.company import CompanyTable
from src.models.entities.transaction import TransactionTable
from src.schemas.create_company_schema import CreateCompanySchema


class ICompanyRepository(ABC):
    @abstractmethod
    def create_company(self, company: CreateCompanySchema) -> CompanyTable:
        pass

    @abstractmethod
    def get_company(self, company_id: UUID) -> CompanyTable | None:
        pass

    @abstractmethod
    def update_balance(self, company_id: UUID, value: float) -> None:
        pass

    @abstractmethod
    def get_statement(
        self, client_id: UUID, client_type: ClientType
    ) -> list[TransactionTable]:
        pass
