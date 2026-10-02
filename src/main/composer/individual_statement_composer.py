from src.controllers.statement_controller import StatementController
from src.database.connection import db_connection_handler
from src.models.repositories.individual_repository import IndividualRepository
from src.models.repositories.transaction_repository import TransactionRepository
from src.services.individual_service import IndividualService
from src.views.statement_view import StatementView


def individual_statement_composer():
    individual_repository = IndividualRepository(db_connection_handler)
    transaction_repository = TransactionRepository(db_connection_handler)
    service = IndividualService(individual_repository, transaction_repository)
    controller = StatementController(service)
    view = StatementView(controller)

    return view
