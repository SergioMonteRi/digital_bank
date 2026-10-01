from src.controllers.interfaces.create_individual_controller import (
    CreateIndividualControllerInterface,
)
from src.models.entities.individual import IndividualTable
from src.schemas.create_individual_schema import CreateIndividualSchema
from src.services.interfaces.individual_service import IndividualServiceInterface


class CreateIndividualController(CreateIndividualControllerInterface):
    def __init__(
        self,
        individual_service: IndividualServiceInterface,
    ):
        self.__individual_service = individual_service

    def create_individual(
        self, individual_data: CreateIndividualSchema
    ) -> IndividualTable:
        return self.__individual_service.create_client(individual_data)
