from abc import ABC, abstractmethod
from uuid import UUID

from src.models.entities.company import CompanyTable


class GetCompanyControllerInterface(ABC):
    @abstractmethod
    def get_company(self, company_id: UUID) -> CompanyTable: ...
