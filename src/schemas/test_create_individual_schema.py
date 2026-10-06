from decimal import Decimal

import pytest
from pydantic import ValidationError

from .create_individual_schema import CreateIndividualSchema


@pytest.fixture(name="valid_body")
def fixture_valid_body():
    return {
        "full_name": "Maria Silva",
        "age": 30,
        "email": "maria.silva@example.com",
        "monthly_income": "10000.00",
        "phone": "11998172371",
    }


class TestCreateIndividualSchema:
    def test_valid(self, valid_body):
        individual = CreateIndividualSchema.model_validate(valid_body)

        assert individual.full_name == "Maria Silva"
        assert individual.monthly_income == Decimal("10000.00")

    def test_strips_whitespace(self, valid_body):
        valid_body["full_name"] = "  Maria Silva  "

        individual = CreateIndividualSchema.model_validate(valid_body)

        assert individual.full_name == "Maria Silva"

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("age", 18),
            ("age", 130),
            ("monthly_income", "0"),
        ],
    )
    def test_accepts_boundary(self, valid_body, field, value):
        valid_body[field] = value

        CreateIndividualSchema.model_validate(valid_body)

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("email", "without-at-sign"),
            ("email", "user@"),
            ("age", 17),
            ("age", 131),
            ("monthly_income", "-0.01"),
            ("monthly_income", "10.555"),
            ("full_name", ""),
            ("full_name", "   "),
            ("full_name", "a" * 256),
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
            CreateIndividualSchema.model_validate(valid_body)

        invalid_fields = {error["loc"][0] for error in exc_info.value.errors()}

        assert invalid_fields == {field}

    @pytest.mark.parametrize(
        "field", ["full_name", "age", "email", "monthly_income", "phone"]
    )
    def test_missing_field(self, valid_body, field):
        del valid_body[field]

        with pytest.raises(ValidationError) as exc_info:
            CreateIndividualSchema.model_validate(valid_body)

        invalid_fields = {error["loc"][0] for error in exc_info.value.errors()}

        assert invalid_fields == {field}

    @pytest.mark.parametrize("phone", ["1133334444", "11998172371", " 11998172371 "])
    def test_accepts_phone(self, valid_body, phone):
        valid_body["phone"] = phone

        individual = CreateIndividualSchema.model_validate(valid_body)

        assert individual.phone == phone.strip()

    def test_rejects_unknown_field(self, valid_body):
        valid_body["category"] = "INDIVIDUAL"

        with pytest.raises(ValidationError) as exc_info:
            CreateIndividualSchema.model_validate(valid_body)

        errors = exc_info.value.errors()

        assert [(error["type"], error["loc"]) for error in errors] == [
            ("extra_forbidden", ("category",))
        ]
