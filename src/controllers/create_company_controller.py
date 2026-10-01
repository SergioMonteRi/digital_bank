from src.controllers.interfaces.create_company_controller import (
    CreateCompanyControllerInterface,
)
from src.models.entities.company import CompanyTable
from src.schemas.create_company_schema import CreateCompanySchema
from src.services.interfaces.company_service import CompanyServiceInterface


class CreateCompanyController(CreateCompanyControllerInterface):
    def __init__(
        self,
        company_service: CompanyServiceInterface,
    ):
        self.__company_service = company_service

    def create_company(self, company_data: CreateCompanySchema) -> CompanyTable:
        return self.__company_service.create_client(company_data)
