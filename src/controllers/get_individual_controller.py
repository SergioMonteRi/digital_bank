from uuid import UUID

from src.controllers.interfaces.get_individual_controller import (
    IGetIndividualController,
)
from src.models.entities.individual import IndividualTable
from src.services.interfaces.individual_service import IndividualServiceInterface


class GetIndividualController(IGetIndividualController):
    def __init__(
        self,
        individual_service: IndividualServiceInterface,
    ):
        self.__individual_service = individual_service

    def get_individual(self, individual_id: UUID) -> IndividualTable | None:
        return self.__individual_service.get_client(individual_id)
