from src.controllers.get_company_controller import GetCompanyController
from src.database.connection import db_connection_handler
from src.models.repositories.company_repository import CompanyRepository
from src.models.repositories.transaction_repository import TransactionRepository
from src.services.company_service import CompanyService
from src.views.get_company_view import GetCompanyView


def get_company_composer():
    company_repository = CompanyRepository(db_connection_handler)
    transaction_repository = TransactionRepository(db_connection_handler)
    service = CompanyService(company_repository, transaction_repository)
    controller = GetCompanyController(service)
    view = GetCompanyView(controller)

    return view
