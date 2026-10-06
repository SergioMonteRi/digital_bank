from decimal import Decimal

from pydantic import BaseModel, Field


class AmountSchema(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
