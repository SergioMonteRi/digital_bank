from unittest.mock import Mock
from uuid import uuid7

import pytest

from src.enum.client_type import ClientType
from src.models.entities.company import CompanyTable
from src.schemas.create_company_schema import CreateCompanySchema


@pytest.fixture(name="company_data")
def fixture_create_company_data():
    data = CreateCompanySchema(
        category=ClientType.COMPANY,
        company_name="NewGo",
        email="newgo.admin@newgo.com.br",
        monthly_revenue=100000,
        phone="11998172371",
    )

    return data


@pytest.fixture(name="company_return_data")
def fixture_create_company_return_data(company_data):
    company_return = CompanyTable(
        id=uuid7(),
        monthly_revenue=company_data.monthly_revenue,
        company_name=company_data.company_name,
        phone=company_data.phone,
        email=company_data.email,
        category=company_data.category,
        balance=0,
    )

    return company_return


@pytest.fixture
def company_repository(company_return_data):
    company_repository_mock = Mock()

    company_repository_mock.create_client.return_value = company_return_data

    company_repository_mock.get_client.return_value = company_return_data

    company_repository_mock.update_balance.return_value = None

    company_repository_mock.calculate_withdraw_limit.return_value = (
        company_return_data.monthly_revenue * 0.9
    )

    return company_repository_mock


@pytest.fixture
def transaction_repository():
    transaction_repository_mock = Mock()
    transaction_repository_mock.create_transaction.return_value = None

    return transaction_repository_mock
