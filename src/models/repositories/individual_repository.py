from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.database.connection import DBConnectionHandler
from src.models.entities.individual import IndividualTable
from src.models.interfaces.individual_repository import IIndividualRepository
from src.schemas.create_individual_schema import CreateIndividualSchema


class IndividualRepository(IIndividualRepository):
    def __init__(self, db_connection: DBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def create_individual(self, individual: CreateIndividualSchema) -> IndividualTable:
        with self.__db_connection as session:
            try:
                individual_data = IndividualTable(
                    monthly_income=individual.monthly_income,
                    age=individual.age,
                    full_name=individual.full_name,
                    phone=individual.phone,
                    email=individual.email,
                    category=individual.category,
                    balance=0,
                )

                session.add(individual_data)
                session.commit()

                return individual_data

            except SQLAlchemyError:
                session.rollback()
                raise

    def get_individual(self, individual_id: int) -> IndividualTable | None:
        with self.__db_connection as session:
            stmt = select(IndividualTable).where(IndividualTable.id == individual_id)

            company = session.scalar(stmt)

            return company
