from src.controllers.withdraw_controller import WithdrawController
from src.database.connection import db_connection_handler
from src.models.repositories.individual_repository import IndividualRepository
from src.models.repositories.transaction_repository import TransactionRepository
from src.services.individual_service import IndividualService
from src.views.withdraw_view import WithdrawView


def individual_withdraw_composer():
    individual_repository = IndividualRepository(db_connection_handler)
    transaction_repository = TransactionRepository(db_connection_handler)
    service = IndividualService(individual_repository, transaction_repository)
    controller = WithdrawController(service)
    view = WithdrawView(controller)

    return view
