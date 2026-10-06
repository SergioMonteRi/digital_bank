from decimal import Decimal

import pytest

from src.schemas.create_company_schema import CreateCompanySchema
from src.schemas.create_individual_schema import CreateIndividualSchema


@pytest.fixture
def company_data():
    data = CreateCompanySchema(
        company_name="NewGo",
        email="newgo.admin@newgo.com.br",
        monthly_revenue=Decimal("100000.00"),
        phone="11998172371",
    )

    return data


@pytest.fixture
def individual_data():
    data = CreateIndividualSchema(
        full_name="Maria Silva",
        age=30,
        email="maria.silva@example.com",
        monthly_income=Decimal("10000.00"),
        phone="11998172371",
    )

    return data
