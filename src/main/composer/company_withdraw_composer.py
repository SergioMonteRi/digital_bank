from src.controllers.withdraw_controller import WithdrawController
from src.database.connection import db_connection_handler
from src.models.repositories.company_repository import CompanyRepository
from src.models.repositories.transaction_repository import TransactionRepository
from src.services.company_service import CompanyService
from src.views.withdraw_view import WithdrawView


def company_withdraw_composer():
    company_repository = CompanyRepository(db_connection_handler)
    transaction_repository = TransactionRepository(db_connection_handler)
    service = CompanyService(company_repository, transaction_repository)
    controller = WithdrawController(service)
    view = WithdrawView(controller)

    return view
