from uuid import UUID

from sqlalchemy import select

from src.database.connection import DBConnectionHandler
from src.exceptions.domain.company_not_found import CompanyNotFound
from src.models.entities.company import CompanyTable
from src.models.entities.transaction import TransactionTable
from src.models.interfaces.client_repository import ClientRepositoryInterface
from src.schemas.create_company_schema import CreateCompanySchema
from src.schemas.create_transaction_schema import CreateTransactionSchema


class CompanyRepository(ClientRepositoryInterface[CompanyTable]):
    def __init__(self, db_connection: DBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def create_client(self, client: CreateCompanySchema) -> CompanyTable:
        with self.__db_connection.get_session() as session:
            company_data = CompanyTable(
                monthly_revenue=client.monthly_revenue,
                company_name=client.company_name,
                phone=client.phone,
                email=client.email,
                category=client.category,
                balance=0,
            )

            session.add(company_data)
            session.commit()

            return company_data

    def get_client(self, client_id: UUID) -> CompanyTable | None:
        with self.__db_connection.get_session() as session:
            stmt = select(CompanyTable).where(CompanyTable.id == client_id)

            company = session.scalar(stmt)

            return company

    def apply_transaction(
        self, client_id: UUID, new_balance: float, transaction: CreateTransactionSchema
    ) -> None:
        with self.__db_connection.get_session() as session:
            company = session.get(CompanyTable, client_id)

            if company is None:
                raise CompanyNotFound()

            company.balance = new_balance

            transaction_data = TransactionTable(
                client_id=transaction.client_id,
                client_type=transaction.client_type,
                transaction_type=transaction.transaction_type,
                amount=transaction.amount,
            )

            session.add(transaction_data)
            session.commit()
