from uuid import UUID

from sqlalchemy import select

from src.database.connection import DBConnectionHandler
from src.models.entities.company import CompanyTable
from src.models.interfaces.client_repository import ClientRepositoryInterface
from src.schemas.create_company_schema import CreateCompanySchema


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

    def update_balance(self, client_id: UUID, value: float) -> None:
        with self.__db_connection.get_session() as session:
            company = session.get(CompanyTable, client_id)

            if company is not None:
                company.balance = value
                session.commit()
