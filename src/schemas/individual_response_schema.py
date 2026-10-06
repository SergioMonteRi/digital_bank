from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class IndividualResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    age: int
    monthly_income: Decimal
    phone: str
    email: str
    category: str
    balance: Decimal
