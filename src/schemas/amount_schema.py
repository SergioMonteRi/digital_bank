from pydantic import BaseModel, Field


class AmountSchema(BaseModel):
    amount: float = Field(gt=0, allow_inf_nan=False)
