from abc import ABC, abstractmethod

from src.models.entities.company import CompanyTable
from src.schemas.create_company_schema import CreateCompanySchema


class ICompanyRepository(ABC):
    @abstractmethod
    def create_company(self, company: CreateCompanySchema) -> CompanyTable:
        pass

    @abstractmethod
    def get_company(self, company_id: int) -> CompanyTable | None:
        pass

    @abstractmethod
    def update_balance(self, company_id: int, value: float) -> None:
        pass
