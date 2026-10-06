from uuid import UUID

from src.enum.client_type import ClientType
from src.enum.transaction_type import TransactionType
from src.exceptions.domain.individual_not_found import IndividualNotFound
from src.exceptions.domain.insufficient_balance import InsufficientBalance
from src.exceptions.domain.withdrawal_limit_exceeded import WithdrawalLimitExceeded
from src.models.entities.individual import IndividualTable
from src.models.entities.transaction import TransactionTable
from src.models.interfaces.client_repository import ClientRepositoryInterface
from src.models.interfaces.transaction_repository import TransactionRepositoryInterface
from src.schemas.create_individual_schema import CreateIndividualSchema
from src.schemas.create_transaction_schema import CreateTransactionSchema
from src.services.interfaces.individual_service import (
    IndividualServiceInterface,
)


class IndividualService(IndividualServiceInterface):
    INDIVIDUAL_WITHDRAW_LIMIT = 0.7

    def __init__(
        self,
        individual_repository: ClientRepositoryInterface,
        transaction_repository: TransactionRepositoryInterface,
    ):
        self.__individual_repository = individual_repository
        self.__transaction_repository = transaction_repository

    def create_client(self, client_data: CreateIndividualSchema) -> IndividualTable:
        return self.__individual_repository.create_client(client_data)

    def get_client(self, client_id: UUID) -> IndividualTable:
        individual = self.__individual_repository.get_client(client_id)

        if individual is None:
            raise IndividualNotFound

        return individual

    def calculate_withdraw_limit(self, monthly_revenue: float) -> float:
        return monthly_revenue * self.INDIVIDUAL_WITHDRAW_LIMIT

    def deposit(self, client_id: UUID, amount: float) -> None:
        individual = self.get_client(client_id)

        new_balance = individual.balance + amount

        transaction_data = CreateTransactionSchema(
            client_id=individual.id,
            client_type=ClientType.INDIVIDUAL,
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
        )

        self.__individual_repository.apply_transaction(
            client_id, new_balance, transaction_data
        )

    def withdraw(self, client_id: UUID, amount: float) -> None:
        individual = self.get_client(client_id)

        if amount > individual.balance:
            raise InsufficientBalance

        withdraw_limit = self.calculate_withdraw_limit(individual.monthly_income)

        if amount > withdraw_limit:
            raise WithdrawalLimitExceeded

        new_balance = individual.balance - amount

        transaction_data = CreateTransactionSchema(
            client_id=individual.id,
            client_type=ClientType.INDIVIDUAL,
            transaction_type=TransactionType.WITHDRAW,
            amount=amount,
        )

        self.__individual_repository.apply_transaction(
            client_id, new_balance, transaction_data
        )

    def statement(self, client_id: UUID) -> list[TransactionTable]:
        self.get_client(client_id)

        return self.__transaction_repository.get_statement(
            client_id, ClientType.INDIVIDUAL
        )
