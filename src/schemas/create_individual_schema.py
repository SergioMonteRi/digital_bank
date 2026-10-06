from decimal import Decimal

from pydantic import Field

from .create_client_base_schema import CreateClientBaseSchema


class CreateIndividualSchema(CreateClientBaseSchema):
    monthly_income: Decimal = Field(max_digits=12, decimal_places=2, ge=0)
    age: int = Field(ge=18, le=130)
    full_name: str
