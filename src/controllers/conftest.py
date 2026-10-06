from unittest.mock import Mock

import pytest

from src.services.interfaces.account_operations import AccountOperationsInterface
from src.services.interfaces.company_service import CompanyServiceInterface
from src.services.interfaces.individual_service import IndividualServiceInterface


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
