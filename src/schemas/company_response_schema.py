from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CompanyResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_name: str
    monthly_revenue: Decimal
    phone: str
    email: str
    balance: Decimal
