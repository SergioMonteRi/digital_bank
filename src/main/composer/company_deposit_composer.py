from src.controllers.deposit_controller import DepositController
from src.database.connection import db_connection_handler
from src.models.repositories.company_repository import CompanyRepository
from src.models.repositories.transaction_repository import TransactionRepository
from src.services.company_service import CompanyService
from src.views.deposit_view import DepositView


def company_deposit_composer():
    company_repository = CompanyRepository(db_connection_handler)
    transaction_repository = TransactionRepository(db_connection_handler)
    service = CompanyService(company_repository, transaction_repository)
    controller = DepositController(service)
    view = DepositView(controller)

    return view
