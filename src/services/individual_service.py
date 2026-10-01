from uuid import UUID

from src.enum.client_type import ClientType
from src.models.entities.individual import IndividualTable
from src.models.entities.transaction import TransactionTable
from src.models.interfaces.client import ClientInterface
from src.models.interfaces.client_repository import ClientRepositoryInterface
from src.schemas.create_individual_schema import CreateIndividualSchema


class IndividualService(ClientInterface[IndividualTable]):
    INDIVIDUAL_WITHDRAW_LIMIT = 0.7

    def __init__(self, individual_repository: ClientRepositoryInterface):
        self.__individual_repository = individual_repository

    def create_individual(
        self, individual: CreateIndividualSchema
    ) -> IndividualTable | None:
        return self.__individual_repository.create_client(individual)

    def get_individual(self, client_id: UUID) -> IndividualTable | None:
        return self.__individual_repository.get_client(client_id)

    def update_balance(self, company_id: UUID, value: float) -> None:
        self.__individual_repository.update_balance(company_id, value)

    def calculate_withdraw_limit(self, monthly_revenue: float) -> float:
        return monthly_revenue * self.INDIVIDUAL_WITHDRAW_LIMIT

    def withdraw(self, client_id: UUID, amount: float) -> None:
        individual = self.get_individual(client_id)

        if individual is None:
            raise Exception

        if amount > individual.balance:
            raise Exception

        withdraw_limit = self.calculate_withdraw_limit(individual.monthly_income)

        if amount > withdraw_limit:
            raise Exception

        new_balance = individual.balance - amount

        self.update_balance(client_id, new_balance)

    def statement(self, client_id: UUID) -> list[TransactionTable]:
        return self.__individual_repository.get_statement(client_id, ClientType.COMPANY)
