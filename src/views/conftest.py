from unittest.mock import Mock

import pytest

from src.controllers.interfaces.create_company_controller import (
    CreateCompanyControllerInterface,
)
from src.controllers.interfaces.create_individual_controller import (
    CreateIndividualControllerInterface,
)
from src.controllers.interfaces.deposit_controller import DepositControllerInterface
from src.controllers.interfaces.get_company_controller import (
    GetCompanyControllerInterface,
)
from src.controllers.interfaces.get_individual_controller import (
    GetIndividualControllerInterface,
)
from src.controllers.interfaces.statement_controller import (
    StatementControllerInterface,
)
from src.controllers.interfaces.withdraw_controller import WithdrawControllerInterface


@pytest.fixture
def company_body():
    body = {
        "category": "COMPANY",
        "company_name": "NewGo",
        "email": "newgo.admin@newgo.com.br",
        "monthly_revenue": 100000,
        "phone": "11998172371",
    }

    return body


@pytest.fixture
def individual_body():
    body = {
        "category": "INDIVIDUAL",
        "full_name": "Maria Silva",
        "age": 30,
        "email": "maria.silva@example.com",
        "monthly_income": 10000,
        "phone": "11998172371",
    }

    return body


@pytest.fixture
def create_company_controller():
    create_company_controller_mock = Mock(spec=CreateCompanyControllerInterface)

    return create_company_controller_mock


@pytest.fixture
def create_individual_controller():
    create_individual_controller_mock = Mock(spec=CreateIndividualControllerInterface)

    return create_individual_controller_mock


@pytest.fixture
def get_company_controller():
    get_company_controller_mock = Mock(spec=GetCompanyControllerInterface)

    return get_company_controller_mock


@pytest.fixture
def get_individual_controller():
    get_individual_controller_mock = Mock(spec=GetIndividualControllerInterface)

    return get_individual_controller_mock


@pytest.fixture
def deposit_controller():
    deposit_controller_mock = Mock(spec=DepositControllerInterface)

    return deposit_controller_mock


@pytest.fixture
def withdraw_controller():
    withdraw_controller_mock = Mock(spec=WithdrawControllerInterface)

    return withdraw_controller_mock


@pytest.fixture
def statement_controller():
    statement_controller_mock = Mock(spec=StatementControllerInterface)

    return statement_controller_mock
