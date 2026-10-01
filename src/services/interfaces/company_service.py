from abc import abstractmethod
from uuid import UUID

from src.models.entities.company import CompanyTable
from src.schemas.create_company_schema import CreateCompanySchema

from .account_operations import AccountOperationsInterface


class CompanyServiceInterface(AccountOperationsInterface):
    @abstractmethod
    def create_client(
        self,
        client_data: CreateCompanySchema,
    ) -> CompanyTable: ...

    @abstractmethod
    def get_client(
        self,
        client_id: UUID,
    ) -> CompanyTable: ...
