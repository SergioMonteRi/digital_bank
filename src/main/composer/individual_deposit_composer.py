from src.controllers.deposit_controller import DepositController
from src.database.connection import db_connection_handler
from src.models.repositories.individual_repository import IndividualRepository
from src.models.repositories.transaction_repository import TransactionRepository
from src.services.individual_service import IndividualService
from src.views.deposit_view import DepositView


def individual_deposit_composer():
    individual_repository = IndividualRepository(db_connection_handler)
    transaction_repository = TransactionRepository(db_connection_handler)
    service = IndividualService(individual_repository, transaction_repository)
    controller = DepositController(service)
    view = DepositView(controller)

    return view
