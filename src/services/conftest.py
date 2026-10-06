from unittest.mock import Mock
from uuid import uuid7

import pytest

from src.enum.client_type import ClientType
from src.models.entities.company import CompanyTable
from src.models.entities.individual import IndividualTable
from src.models.interfaces.client_repository import ClientRepositoryInterface
from src.models.interfaces.transaction_repository import TransactionRepositoryInterface
from src.schemas.create_company_schema import CreateCompanySchema
from src.schemas.create_individual_schema import CreateIndividualSchema


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
    company_repository_mock = Mock(spec=ClientRepositoryInterface)

    company_repository_mock.create_client.return_value = company_return_data

    company_repository_mock.get_client.return_value = company_return_data

    return company_repository_mock


@pytest.fixture(name="individual_data")
def fixture_create_individual_data():
    data = CreateIndividualSchema(
        category=ClientType.INDIVIDUAL,
        full_name="Maria Silva",
        age=30,
        email="maria.silva@example.com",
        monthly_income=10000,
        phone="11998172371",
    )

    return data


@pytest.fixture(name="individual_return_data")
def fixture_create_individual_return_data(individual_data):
    individual_return = IndividualTable(
        id=uuid7(),
        monthly_income=individual_data.monthly_income,
        age=individual_data.age,
        full_name=individual_data.full_name,
        phone=individual_data.phone,
        email=individual_data.email,
        category=individual_data.category,
        balance=0,
    )

    return individual_return


@pytest.fixture
def individual_repository(individual_return_data):
    individual_repository_mock = Mock(spec=ClientRepositoryInterface)

    individual_repository_mock.create_client.return_value = individual_return_data

    individual_repository_mock.get_client.return_value = individual_return_data

    return individual_repository_mock


@pytest.fixture
def transaction_repository():
    transaction_repository_mock = Mock(spec=TransactionRepositoryInterface)

    return transaction_repository_mock
