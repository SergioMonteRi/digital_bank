from src.controllers.get_individual_controller import GetIndividualController
from src.database.connection import db_connection_handler
from src.models.repositories.individual_repository import IndividualRepository
from src.models.repositories.transaction_repository import TransactionRepository
from src.services.individual_service import IndividualService
from src.views.get_individual_view import GetIndividualView


def get_individual_composer():
    individual_repository = IndividualRepository(db_connection_handler)
    transaction_repository = TransactionRepository(db_connection_handler)
    service = IndividualService(individual_repository, transaction_repository)
    controller = GetIndividualController(service)
    view = GetIndividualView(controller)

    return view
