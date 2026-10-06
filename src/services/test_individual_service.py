from uuid import UUID

import pytest

from src.enum.client_type import ClientType
from src.enum.transaction_type import TransactionType
from src.exceptions.domain.individual_not_found import IndividualNotFound
from src.exceptions.domain.insufficient_balance import InsufficientBalance
from src.exceptions.domain.withdrawal_limit_exceeded import WithdrawalLimitExceeded
from src.schemas.create_transaction_schema import CreateTransactionSchema

from .individual_service import IndividualService


class TestIndividualService:
    def test_create_client(
        self, individual_repository, transaction_repository, individual_data
    ):
        service = IndividualService(individual_repository, transaction_repository)
        response = service.create_client(individual_data)

        individual_repository.create_client.assert_called_once_with(individual_data)

        assert response is individual_repository.create_client.return_value

    def test_get_client(self, individual_repository, transaction_repository):
        service = IndividualService(individual_repository, transaction_repository)

        client_id = individual_repository.get_client.return_value.id

        selected_client = service.get_client(client_id)

        individual_repository.get_client.assert_called_once_with(client_id)

        assert selected_client is individual_repository.get_client.return_value

    def test_get_client_not_found(self, individual_repository, transaction_repository):
        individual_repository.get_client.return_value = None

        service = IndividualService(individual_repository, transaction_repository)

        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        with pytest.raises(IndividualNotFound):
            service.get_client(client_id)

        individual_repository.get_client.assert_called_once_with(client_id)

    def test_deposit(self, individual_repository, transaction_repository):
        deposit_amount = 1000
        expected_balance = 1500

        client_id = individual_repository.get_client.return_value.id
        individual_repository.get_client.return_value.balance = 500

        expected_transaction = CreateTransactionSchema(
            client_id=client_id,
            client_type=ClientType.INDIVIDUAL,
            transaction_type=TransactionType.DEPOSIT,
            amount=deposit_amount,
        )

        service = IndividualService(individual_repository, transaction_repository)

        service.deposit(client_id, deposit_amount)

        individual_repository.get_client.assert_called_once_with(client_id)

        individual_repository.apply_transaction.assert_called_once_with(
            client_id, expected_balance, expected_transaction
        )

    def test_deposit_client_not_found(
        self, individual_repository, transaction_repository
    ):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")
        deposit_amount = 1000

        individual_repository.get_client.return_value = None

        service = IndividualService(individual_repository, transaction_repository)

        with pytest.raises(IndividualNotFound):
            service.deposit(client_id, deposit_amount)

        individual_repository.get_client.assert_called_once_with(client_id)

        individual_repository.apply_transaction.assert_not_called()

    def test_withdraw(self, individual_repository, transaction_repository):
        withdraw_amount = 7000
        expected_balance = 3000

        client_id = individual_repository.get_client.return_value.id
        individual_repository.get_client.return_value.balance = 10000
        individual_repository.get_client.return_value.monthly_income = 10000

        expected_transaction = CreateTransactionSchema(
            client_id=client_id,
            client_type=ClientType.INDIVIDUAL,
            transaction_type=TransactionType.WITHDRAW,
            amount=withdraw_amount,
        )

        service = IndividualService(individual_repository, transaction_repository)

        service.withdraw(client_id, withdraw_amount)

        individual_repository.get_client.assert_called_once_with(client_id)

        individual_repository.apply_transaction.assert_called_once_with(
            client_id, expected_balance, expected_transaction
        )

    def test_withdraw_insufficient_balance(
        self, individual_repository, transaction_repository
    ):
        withdraw_amount = 5001

        client_id = individual_repository.get_client.return_value.id
        individual_repository.get_client.return_value.balance = 5000
        individual_repository.get_client.return_value.monthly_income = 10000

        service = IndividualService(individual_repository, transaction_repository)

        with pytest.raises(InsufficientBalance):
            service.withdraw(client_id, withdraw_amount)

        individual_repository.get_client.assert_called_once_with(client_id)

        individual_repository.apply_transaction.assert_not_called()

    def test_withdraw_limit_exceeded(
        self, individual_repository, transaction_repository
    ):
        withdraw_amount = 7001

        client_id = individual_repository.get_client.return_value.id
        individual_repository.get_client.return_value.balance = 20000
        individual_repository.get_client.return_value.monthly_income = 10000

        service = IndividualService(individual_repository, transaction_repository)

        with pytest.raises(WithdrawalLimitExceeded):
            service.withdraw(client_id, withdraw_amount)

        individual_repository.get_client.assert_called_once_with(client_id)

        individual_repository.apply_transaction.assert_not_called()

    def test_withdraw_client_not_found(
        self, individual_repository, transaction_repository
    ):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")
        withdraw_amount = 1000

        individual_repository.get_client.return_value = None

        service = IndividualService(individual_repository, transaction_repository)

        with pytest.raises(IndividualNotFound):
            service.withdraw(client_id, withdraw_amount)

        individual_repository.get_client.assert_called_once_with(client_id)

        individual_repository.apply_transaction.assert_not_called()

    def test_statement(self, individual_repository, transaction_repository):
        client_id = individual_repository.get_client.return_value.id

        service = IndividualService(individual_repository, transaction_repository)

        statement = service.statement(client_id)

        individual_repository.get_client.assert_called_once_with(client_id)

        transaction_repository.get_statement.assert_called_once_with(
            client_id, ClientType.INDIVIDUAL
        )

        assert statement is transaction_repository.get_statement.return_value

    def test_statement_client_not_found(
        self, individual_repository, transaction_repository
    ):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        individual_repository.get_client.return_value = None

        service = IndividualService(individual_repository, transaction_repository)

        with pytest.raises(IndividualNotFound):
            service.statement(client_id)

        individual_repository.get_client.assert_called_once_with(client_id)

        transaction_repository.get_statement.assert_not_called()
