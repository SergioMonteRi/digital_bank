from pydantic import BaseModel, Field


class WithdrawSchema(BaseModel):
    amount: float = Field(gt=0, allow_inf_nan=False)
