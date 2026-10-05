from src.controllers.create_company_controller import CreateCompanyController
from src.database.connection import db_connection_handler
from src.models.repositories.company_repository import CompanyRepository
from src.models.repositories.transaction_repository import TransactionRepository
from src.services.company_service import CompanyService
from src.views.create_company_view import CreateCompanyView


def create_company_composer():
    company_repository = CompanyRepository(db_connection_handler)
    transaction_repository = TransactionRepository(db_connection_handler)
    service = CompanyService(company_repository, transaction_repository)
    controller = CreateCompanyController(service)
    view = CreateCompanyView(controller)

    return view
