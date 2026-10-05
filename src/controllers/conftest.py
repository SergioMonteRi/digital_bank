from unittest.mock import Mock

import pytest

from src.enum.client_type import ClientType
from src.schemas.create_company_schema import CreateCompanySchema
from src.schemas.create_individual_schema import CreateIndividualSchema
from src.services.interfaces.account_operations import AccountOperationsInterface
from src.services.interfaces.company_service import CompanyServiceInterface
from src.services.interfaces.individual_service import IndividualServiceInterface


@pytest.fixture
def company_data():
    data = CreateCompanySchema(
        category=ClientType.COMPANY,
        company_name="NewGo",
        email="newgo.admin@newgo.com.br",
        monthly_revenue=100000,
        phone="11998172371",
    )

    return data


@pytest.fixture
def individual_data():
    data = CreateIndividualSchema(
        category=ClientType.INDIVIDUAL,
        full_name="Maria Silva",
        age=30,
        email="maria.silva@example.com",
        monthly_income=10000,
        phone="11998172371",
    )

    return data


@pytest.fixture
def company_service():
    company_service_mock = Mock(spec=CompanyServiceInterface)

    return company_service_mock


@pytest.fixture
def individual_service():
    individual_service_mock = Mock(spec=IndividualServiceInterface)

    return individual_service_mock


@pytest.fixture
def client_service():
    client_service_mock = Mock(spec=AccountOperationsInterface)

    return client_service_mock
