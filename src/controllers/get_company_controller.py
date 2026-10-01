from uuid import UUID

from src.controllers.interfaces.get_company_controller import (
    GetCompanyControllerInterface,
)
from src.models.entities.company import CompanyTable
from src.services.interfaces.company_service import CompanyServiceInterface


class GetCompanyController(GetCompanyControllerInterface):
    def __init__(
        self,
        company_service: CompanyServiceInterface,
    ):
        self.__company_service = company_service

    def get_company(self, company_id: UUID) -> CompanyTable:
        return self.__company_service.get_client(company_id)
