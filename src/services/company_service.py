from uuid import UUID

from src.enum.client_type import ClientType
from src.enum.transaction_type import TransactionType
from src.exceptions.domain.company_not_found import CompanyNotFound
from src.exceptions.domain.insufficient_balance import InsufficientBalance
from src.exceptions.domain.withdrawal_limit_exceeded import WithdrawalLimitExceeded
from src.models.entities.company import CompanyTable
from src.models.entities.transaction import TransactionTable
from src.models.interfaces.client_repository import ClientRepositoryInterface
from src.models.interfaces.transaction_repository import TransactionRepositoryInterface
from src.schemas.create_company_schema import CreateCompanySchema
from src.schemas.create_transaction_schema import CreateTransactionSchema
from src.services.interfaces.company_service import CompanyServiceInterface


class CompanyService(CompanyServiceInterface):
    COMPANY_WITHDRAW_LIMIT = 0.9

    def __init__(
        self,
        company_repository: ClientRepositoryInterface,
        transaction_repository: TransactionRepositoryInterface,
    ):
        self.__company_repository = company_repository
        self.__transaction_repository = transaction_repository

    def create_client(self, client_data: CreateCompanySchema) -> CompanyTable:
        return self.__company_repository.create_client(client_data)

    def get_company(self, client_id: UUID) -> CompanyTable | None:
        return self.__company_repository.get_client(client_id)

    def update_balance(self, client_id: UUID, amount: float) -> None:
        self.__company_repository.update_balance(client_id, amount)

    def calculate_withdraw_limit(self, monthly_revenue: float) -> float:
        return monthly_revenue * self.COMPANY_WITHDRAW_LIMIT

    def withdraw(self, client_id: UUID, amount: float) -> None:
        company = self.get_company(client_id)

        if company is None:
            raise CompanyNotFound

        if amount > company.balance:
            raise InsufficientBalance

        withdraw_limit = self.calculate_withdraw_limit(company.monthly_revenue)

        if amount > withdraw_limit:
            raise WithdrawalLimitExceeded

        new_balance = company.balance - amount

        self.update_balance(client_id, new_balance)

        transaction_data = CreateTransactionSchema(
            client_id=company.id,
            client_type=ClientType.COMPANY,
            transaction_type=TransactionType.WITHDRAW,
            amount=amount,
        )

        self.__transaction_repository.create_transaction(transaction_data)

    def statement(self, client_id: UUID) -> list[TransactionTable]:
        return self.__transaction_repository.get_statement(
            client_id, ClientType.COMPANY
        )
