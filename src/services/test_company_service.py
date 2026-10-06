from decimal import Decimal
from uuid import UUID

import pytest

from src.enum.client_type import ClientType
from src.enum.transaction_type import TransactionType
from src.exceptions.domain.company_not_found import CompanyNotFound
from src.exceptions.domain.insufficient_balance import InsufficientBalance
from src.exceptions.domain.withdrawal_limit_exceeded import WithdrawalLimitExceeded
from src.schemas.create_transaction_schema import CreateTransactionSchema

from .company_service import CompanyService


class TestCompanyService:
    def test_create_client(
        self, company_repository, transaction_repository, company_data
    ):
        service = CompanyService(company_repository, transaction_repository)
        response = service.create_client(company_data)

        company_repository.create_client.assert_called_once_with(company_data)

        assert response is company_repository.create_client.return_value

    def test_get_client(self, company_repository, transaction_repository):
        service = CompanyService(company_repository, transaction_repository)

        client_id = company_repository.get_client.return_value.id

        selected_client = service.get_client(client_id)

        company_repository.get_client.assert_called_once_with(client_id)

        assert selected_client is company_repository.get_client.return_value

    def test_get_client_not_found(self, company_repository, transaction_repository):
        company_repository.get_client.return_value = None

        service = CompanyService(company_repository, transaction_repository)

        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        with pytest.raises(CompanyNotFound):
            service.get_client(client_id)

        company_repository.get_client.assert_called_once_with(client_id)

    def test_deposit(self, company_repository, transaction_repository):
        deposit_amount = Decimal("10000.00")

        client_id = company_repository.get_client.return_value.id
        company_repository.get_client.return_value.balance = Decimal("5000.00")

        expected_transaction = CreateTransactionSchema(
            client_id=client_id,
            client_type=ClientType.COMPANY,
            transaction_type=TransactionType.DEPOSIT,
            amount=deposit_amount,
        )

        service = CompanyService(company_repository, transaction_repository)

        service.deposit(client_id, deposit_amount)

        company_repository.get_client.assert_called_once_with(client_id)

        company_repository.apply_transaction.assert_called_once_with(
            expected_transaction
        )

    def test_deposit_client_not_found(self, company_repository, transaction_repository):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")
        deposit_amount = Decimal("10000.00")

        company_repository.get_client.return_value = None

        service = CompanyService(company_repository, transaction_repository)

        with pytest.raises(CompanyNotFound):
            service.deposit(client_id, deposit_amount)

        company_repository.get_client.assert_called_once_with(client_id)

        company_repository.apply_transaction.assert_not_called()

    def test_withdraw(self, company_repository, transaction_repository):
        withdraw_amount = Decimal("90000.00")

        client_id = company_repository.get_client.return_value.id
        company_repository.get_client.return_value.balance = Decimal("100000.00")

        expected_transaction = CreateTransactionSchema(
            client_id=client_id,
            client_type=ClientType.COMPANY,
            transaction_type=TransactionType.WITHDRAW,
            amount=withdraw_amount,
        )

        service = CompanyService(company_repository, transaction_repository)

        service.withdraw(client_id, withdraw_amount)

        company_repository.get_client.assert_called_once_with(client_id)

        company_repository.apply_transaction.assert_called_once_with(
            expected_transaction
        )

    def test_withdraw_insufficient_balance(
        self, company_repository, transaction_repository
    ):
        withdraw_amount = Decimal("5001.00")

        client_id = company_repository.get_client.return_value.id
        company_repository.get_client.return_value.balance = Decimal("5000.00")
        company_repository.get_client.return_value.monthly_revenue = Decimal(
            "100000.00"
        )

        service = CompanyService(company_repository, transaction_repository)

        with pytest.raises(InsufficientBalance):
            service.withdraw(client_id, withdraw_amount)

        company_repository.get_client.assert_called_once_with(client_id)

        company_repository.apply_transaction.assert_not_called()

    def test_withdraw_limit_exceeded(self, company_repository, transaction_repository):
        withdraw_amount = Decimal("90001.00")

        client_id = company_repository.get_client.return_value.id
        company_repository.get_client.return_value.balance = Decimal("200000.00")
        company_repository.get_client.return_value.monthly_revenue = Decimal(
            "100000.00"
        )

        service = CompanyService(company_repository, transaction_repository)

        with pytest.raises(WithdrawalLimitExceeded):
            service.withdraw(client_id, withdraw_amount)

        company_repository.get_client.assert_called_once_with(client_id)

        company_repository.apply_transaction.assert_not_called()

    def test_withdraw_client_not_found(
        self, company_repository, transaction_repository
    ):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")
        withdraw_amount = Decimal("10000.00")

        company_repository.get_client.return_value = None

        service = CompanyService(company_repository, transaction_repository)

        with pytest.raises(CompanyNotFound):
            service.withdraw(client_id, withdraw_amount)

        company_repository.get_client.assert_called_once_with(client_id)

        company_repository.apply_transaction.assert_not_called()

    def test_statement(self, company_repository, transaction_repository):
        client_id = company_repository.get_client.return_value.id

        service = CompanyService(company_repository, transaction_repository)

        statement = service.statement(client_id)

        company_repository.get_client.assert_called_once_with(client_id)

        transaction_repository.get_statement.assert_called_once_with(
            client_id, ClientType.COMPANY
        )

        assert statement is transaction_repository.get_statement.return_value

    def test_statement_client_not_found(
        self, company_repository, transaction_repository
    ):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        company_repository.get_client.return_value = None

        service = CompanyService(company_repository, transaction_repository)

        with pytest.raises(CompanyNotFound):
            service.statement(client_id)

        company_repository.get_client.assert_called_once_with(client_id)

        transaction_repository.get_statement.assert_not_called()

    def test_calculate_withdraw_limit_rounds_down(
        self, company_repository, transaction_repository
    ):
        service = CompanyService(company_repository, transaction_repository)

        withdraw_limit = service.calculate_withdraw_limit(Decimal("1000.15"))

        assert withdraw_limit == Decimal("900.13")
