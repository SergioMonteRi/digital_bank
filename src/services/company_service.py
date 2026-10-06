from decimal import ROUND_DOWN, Decimal
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
    COMPANY_WITHDRAW_LIMIT = Decimal("0.9")

    def __init__(
        self,
        company_repository: ClientRepositoryInterface[
            CompanyTable, CreateCompanySchema
        ],
        transaction_repository: TransactionRepositoryInterface,
    ):
        self.__company_repository = company_repository
        self.__transaction_repository = transaction_repository

    def create_client(self, client_data: CreateCompanySchema) -> CompanyTable:
        return self.__company_repository.create_client(client_data)

    def get_client(self, client_id: UUID) -> CompanyTable:
        company = self.__company_repository.get_client(client_id)

        if company is None:
            raise CompanyNotFound

        return company

    def calculate_withdraw_limit(self, monthly_revenue: Decimal) -> Decimal:
        return (monthly_revenue * self.COMPANY_WITHDRAW_LIMIT).quantize(
            exp=Decimal("0.01"), rounding=ROUND_DOWN
        )

    def deposit(self, client_id: UUID, amount: Decimal) -> None:
        company = self.get_client(client_id)

        transaction_data = CreateTransactionSchema(
            client_id=company.id,
            client_type=ClientType.COMPANY,
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
        )

        self.__company_repository.apply_transaction(transaction_data)

    def withdraw(self, client_id: UUID, amount: Decimal) -> None:
        company = self.get_client(client_id)

        if amount > company.balance:
            raise InsufficientBalance

        withdraw_limit = self.calculate_withdraw_limit(company.monthly_revenue)

        if amount > withdraw_limit:
            raise WithdrawalLimitExceeded

        transaction_data = CreateTransactionSchema(
            client_id=company.id,
            client_type=ClientType.COMPANY,
            transaction_type=TransactionType.WITHDRAW,
            amount=amount,
        )

        self.__company_repository.apply_transaction(transaction_data)

    def statement(self, client_id: UUID) -> list[TransactionTable]:
        self.get_client(client_id)

        return self.__transaction_repository.get_statement(
            client_id, ClientType.COMPANY
        )
