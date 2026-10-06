from decimal import Decimal

import pytest
from pydantic import ValidationError

from .create_company_schema import CreateCompanySchema


@pytest.fixture(name="valid_body")
def fixture_valid_body():
    return {
        "company_name": "NewGo",
        "email": "newgo.admin@newgo.com.br",
        "monthly_revenue": "100000.00",
        "phone": "11998172371",
    }


class TestCreateCompanySchema:
    def test_valid(self, valid_body):
        company = CreateCompanySchema.model_validate(valid_body)

        assert company.company_name == "NewGo"
        assert company.monthly_revenue == Decimal("100000.00")

    def test_strips_whitespace(self, valid_body):
        valid_body["company_name"] = "  NewGo  "

        company = CreateCompanySchema.model_validate(valid_body)

        assert company.company_name == "NewGo"

    def test_accepts_zero_revenue(self, valid_body):
        valid_body["monthly_revenue"] = "0"

        company = CreateCompanySchema.model_validate(valid_body)

        assert company.monthly_revenue == Decimal("0")

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("email", "without-at-sign"),
            ("email", "user@"),
            ("monthly_revenue", "-0.01"),
            ("monthly_revenue", "10.555"),
            ("company_name", ""),
            ("company_name", "   "),
            ("company_name", "a" * 256),
            ("phone", ""),
            ("phone", "   "),
            ("phone", "119981723"),
            ("phone", "119981723712"),
            ("phone", "(11) 99817-2371"),
            ("phone", "1199817237a"),
        ],
    )
    def test_invalid_field(self, valid_body, field, value):
        valid_body[field] = value

        with pytest.raises(ValidationError) as exc_info:
            CreateCompanySchema.model_validate(valid_body)

        invalid_fields = {error["loc"][0] for error in exc_info.value.errors()}

        assert invalid_fields == {field}

    @pytest.mark.parametrize(
        "field", ["company_name", "email", "monthly_revenue", "phone"]
    )
    def test_missing_field(self, valid_body, field):
        del valid_body[field]

        with pytest.raises(ValidationError) as exc_info:
            CreateCompanySchema.model_validate(valid_body)

        invalid_fields = {error["loc"][0] for error in exc_info.value.errors()}

        assert invalid_fields == {field}

    @pytest.mark.parametrize("phone", ["1133334444", "11998172371", " 11998172371 "])
    def test_accepts_phone(self, valid_body, phone):
        valid_body["phone"] = phone

        company = CreateCompanySchema.model_validate(valid_body)

        assert company.phone == phone.strip()

    def test_rejects_unknown_field(self, valid_body):
        valid_body["category"] = "COMPANY"

        with pytest.raises(ValidationError) as exc_info:
            CreateCompanySchema.model_validate(valid_body)

        errors = exc_info.value.errors()

        assert [(error["type"], error["loc"]) for error in errors] == [
            ("extra_forbidden", ("category",))
        ]
