from decimal import Decimal

from pydantic import BaseModel, Field


class CreateIndividualSchema(BaseModel):
    monthly_income: Decimal = Field(max_digits=12, decimal_places=2)
    age: int
    full_name: str
    phone: str
    email: str
    category: str
