from abc import ABC, abstractmethod

from src.models.entities.company import CompanyTable
from src.schemas.create_company_schema import CreateCompanySchema


class CreateCompanyControllerInterface(ABC):
    @abstractmethod
    def create_company(self, company_data: CreateCompanySchema) -> CompanyTable: ...
