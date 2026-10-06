from uuid import UUID

from sqlalchemy import select, update

from src.database.connection import DBConnectionHandler
from src.enum.transaction_type import TransactionType
from src.exceptions.domain.individual_not_found import IndividualNotFound
from src.exceptions.domain.insufficient_balance import InsufficientBalance
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

    def apply_transaction(self, transaction: CreateTransactionSchema) -> None:
        with self.__db_connection.get_session() as session:
            individual = session.get(IndividualTable, transaction.client_id)

            if individual is None:
                raise IndividualNotFound()

            stmt = update(IndividualTable).where(
                IndividualTable.id == transaction.client_id
            )

            if transaction.transaction_type == TransactionType.WITHDRAW:
                withdraw_stmt = (
                    stmt.where(IndividualTable.balance >= transaction.amount)
                    .values(balance=IndividualTable.balance - transaction.amount)
                    .returning(IndividualTable.id)
                )

                updated_id = session.execute(withdraw_stmt).scalar_one_or_none()

                if updated_id is None:
                    raise InsufficientBalance()

            elif transaction.transaction_type == TransactionType.DEPOSIT:
                deposit_stmt = stmt.values(
                    balance=IndividualTable.balance + transaction.amount
                )

                session.execute(deposit_stmt)

            else:
                raise ValueError(
                    f"Unsupported transaction type: {transaction.transaction_type}"
                )

            transaction_data = TransactionTable(
                client_id=transaction.client_id,
                client_type=transaction.client_type,
                transaction_type=transaction.transaction_type,
                amount=transaction.amount,
            )

            session.add(transaction_data)
            session.commit()
