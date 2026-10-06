from uuid import UUID

from sqlalchemy import select, update

from src.database.connection import DBConnectionHandler
from src.enum.transaction_type import TransactionType
from src.exceptions.domain.company_not_found import CompanyNotFound
from src.exceptions.domain.insufficient_balance import InsufficientBalance
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

    def apply_transaction(self, transaction: CreateTransactionSchema) -> None:
        with self.__db_connection.get_session() as session:
            company = session.get(CompanyTable, transaction.client_id)

            if company is None:
                raise CompanyNotFound()

            stmt = update(CompanyTable).where(CompanyTable.id == transaction.client_id)

            if transaction.transaction_type == TransactionType.WITHDRAW:
                withdraw_stmt = (
                    stmt.where(CompanyTable.balance >= transaction.amount)
                    .values(balance=CompanyTable.balance - transaction.amount)
                    .returning(CompanyTable.id)
                )

                updated_id = session.execute(withdraw_stmt).scalar_one_or_none()

                if updated_id is None:
                    raise InsufficientBalance()

            elif transaction.transaction_type == TransactionType.DEPOSIT:
                deposit_stmt = stmt.values(
                    balance=CompanyTable.balance + transaction.amount
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
