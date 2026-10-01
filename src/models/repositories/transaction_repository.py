from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.database.connection import DBConnectionHandler
from src.enum.client_type import ClientType
from src.models.entities.transaction import TransactionTable
from src.models.interfaces.transaction_repository import TransactionRepositoryInterface
from src.schemas.create_transaction_schema import CreateTransactionSchema


class TransactionRepository(TransactionRepositoryInterface):
    def __init__(self, db_connection: DBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def create_transaction(self, transaction: CreateTransactionSchema):
        with self.__db_connection as session:
            try:
                transaction_data = TransactionTable(
                    client_id=transaction.client_id,
                    client_type=transaction.client_type,
                    transaction_type=transaction.transaction_type,
                    amount=transaction.amount,
                )

                session.add(transaction_data)
                session.commit()

                return transaction_data
            except SQLAlchemyError:
                session.rollback()
                raise

    def get_statement(self, client_id: UUID, client_type: ClientType):
        with self.__db_connection as session:
            stmt = (
                select(TransactionTable)
                .where(
                    TransactionTable.client_id == client_id,
                    TransactionTable.client_type == client_type,
                )
                .order_by(TransactionTable.created_at.desc())
            )

            statements = session.scalars(stmt).all()

            return statements
