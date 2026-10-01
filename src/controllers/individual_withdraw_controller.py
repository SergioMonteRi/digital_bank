from uuid import UUID

from src.controllers.interfaces.individual_withdraw_controller import (
    IIndividualWithdrawController,
)
from src.services.interfaces.individual_service import (
    IndividualServiceInterface,
)


class IndividualWithdrawController(IIndividualWithdrawController):
    def __init__(
        self,
        individual_service: IndividualServiceInterface,
    ):
        self.__individual_service = individual_service

    def withdraw(self, client_id: UUID, amount: float) -> None:
        self.__individual_service.withdraw(client_id, amount)
