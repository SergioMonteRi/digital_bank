from decimal import Decimal

from pydantic import BaseModel, Field


class CreateCompanySchema(BaseModel):
    monthly_revenue: Decimal = Field(max_digits=12, decimal_places=2)
    company_name: str
    phone: str
    email: str
    category: str
