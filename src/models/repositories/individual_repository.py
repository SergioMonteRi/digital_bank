from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.database.connection import DBConnectionHandler
from src.enum.client_type import ClientType
from src.models.entities.individual import IndividualTable
from src.models.entities.transaction import TransactionTable
from src.models.interfaces.client_repository import ClientRepositoryInterface
from src.schemas.create_individual_schema import CreateIndividualSchema


class IndividualRepository(ClientRepositoryInterface[IndividualTable]):
    def __init__(self, db_connection: DBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def create_client(self, client: CreateIndividualSchema) -> IndividualTable:
        with self.__db_connection as session:
            try:
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

            except SQLAlchemyError:
                session.rollback()
                raise

    def get_client(self, client_id: UUID) -> IndividualTable | None:
        with self.__db_connection as session:
            stmt = select(IndividualTable).where(IndividualTable.id == client_id)

            company = session.scalar(stmt)

            return company

    def update_balance(self, client_id: UUID, value: float) -> None:
        with self.__db_connection as session:
            company = session.get(IndividualTable, client_id)

            if company is not None:
                company.balance = value
                session.commit()

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

            transactions = session.scalars(stmt).all()

            return transactions
