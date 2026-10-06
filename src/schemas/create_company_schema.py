from decimal import Decimal

from pydantic import Field

from .create_client_base_schema import CreateClientBaseSchema


class CreateCompanySchema(CreateClientBaseSchema):
    monthly_revenue: Decimal = Field(max_digits=12, decimal_places=2, ge=0)
    company_name: str
