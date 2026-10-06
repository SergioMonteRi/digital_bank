from uuid import UUID

from sqlalchemy import select

from src.database.connection import DBConnectionHandler
from src.exceptions.domain.individual_not_found import IndividualNotFound
from src.models.entities.individual import IndividualTable
from src.models.entities.transaction import TransactionTable
from src.models.interfaces.client_repository import ClientRepositoryInterface
from src.schemas.create_individual_schema import CreateIndividualSchema
from src.schemas.create_transaction_schema import CreateTransactionSchema


class IndividualRepository(ClientRepositoryInterface[IndividualTable]):
    def __init__(self, db_connection: DBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def create_client(self, client: CreateIndividualSchema) -> IndividualTable:
        with self.__db_connection.get_session() as session:
            individual_data = IndividualTable(
                monthly_income=client.monthly_income,
                age=client.age,
                full_name=client.full_name,
                phone=client.phone,
                email=client.email,
                category=client.category,
                balance=0,
            )

            session.add(individual_data)
            session.commit()

            return individual_data

    def get_client(self, client_id: UUID) -> IndividualTable | None:
        with self.__db_connection.get_session() as session:
            stmt = select(IndividualTable).where(IndividualTable.id == client_id)

            individual = session.scalar(stmt)

            return individual

    def apply_transaction(
        self, client_id: UUID, new_balance: float, transaction: CreateTransactionSchema
    ) -> None:
        with self.__db_connection.get_session() as session:
            individual = session.get(IndividualTable, client_id)

            if individual is None:
                raise IndividualNotFound()

            individual.balance = new_balance

            transaction_data = TransactionTable(
                client_id=transaction.client_id,
                client_type=transaction.client_type,
                transaction_type=transaction.transaction_type,
                amount=transaction.amount,
            )

            session.add(transaction_data)
            session.commit()
