from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.database.connection import DBConnectionHandler
from src.models.entities.company import CompanyTable
from src.models.interfaces.company_repository import ICompanyRepository
from src.schemas.create_company_schema import CreateCompanySchema


class CompanyRepository(ICompanyRepository):
    def __init__(self, db_connection: DBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def create_company(self, company: CreateCompanySchema) -> CompanyTable:
        with self.__db_connection as session:
            try:
                company_data = CompanyTable(
                    monthly_revenue=company.monthly_revenue,
                    company_name=company.company_name,
                    phone=company.phone,
                    email=company.email,
                    category=company.category,
                    balance=0,
                )

                session.add(company_data)
                session.commit()

                return company_data

            except SQLAlchemyError:
                session.rollback()
                raise

    def get_company(self, company_id: int) -> CompanyTable | None:
        with self.__db_connection as session:
            stmt = select(CompanyTable).where(CompanyTable.id == company_id)

            company = session.scalar(stmt)

            return company

    def update_balance(self, company_id: int, value: float) -> None:
        with self.__db_connection as session:
            company = session.get(CompanyTable, company_id)

            if company is not None:
                company.balance = value
                session.commit()
