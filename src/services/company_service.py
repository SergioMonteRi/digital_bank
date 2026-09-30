from uuid import UUID

from src.enum.client_type import ClientType
from src.models.entities.company import CompanyTable
from src.models.entities.transaction import TransactionTable
from src.models.interfaces.client import ClientInterface
from src.models.interfaces.company_repository import ICompanyRepository
from src.schemas.create_company_schema import CreateCompanySchema


class CompanyService(ClientInterface[CompanyTable]):
    COMPANY_WITHDRAW_LIMIT = 0.9

    def __init__(self, company_repository: ICompanyRepository):
        self.__company_repository = company_repository

    def create_company(self, company: CreateCompanySchema) -> CompanyTable | None:
        return self.__company_repository.create_company(company)

    def get_client(self, client_id: UUID) -> CompanyTable | None:
        return self.__company_repository.get_company(client_id)

    def update_balance(self, company_id: UUID, value: float) -> None:
        self.__company_repository.update_balance(company_id, value)

    def calculate_withdraw_limit(self, monthly_revenue: float) -> float:
        return monthly_revenue * self.COMPANY_WITHDRAW_LIMIT

    def withdraw(self, client_id: UUID, amount: float) -> None:
        company = self.get_client(client_id)

        if company is None:
            raise Exception

        if amount > company.balance:
            raise Exception

        withdraw_limit = self.calculate_withdraw_limit(company.monthly_revenue)

        if amount > withdraw_limit:
            raise Exception

        new_balance = company.balance - amount

        self.update_balance(client_id, new_balance)

    def statement(self, client_id: UUID) -> list[TransactionTable]:
        return self.__company_repository.get_statement(client_id, ClientType.COMPANY)
