from src.controllers.statement_controller import StatementController
from src.database.connection import db_connection_handler
from src.models.repositories.company_repository import CompanyRepository
from src.models.repositories.transaction_repository import TransactionRepository
from src.services.company_service import CompanyService
from src.views.statement_view import StatementView


def company_statement_composer():
    company_repository = CompanyRepository(db_connection_handler)
    transaction_repository = TransactionRepository(db_connection_handler)
    service = CompanyService(company_repository, transaction_repository)
    controller = StatementController(service)
    view = StatementView(controller)

    return view
