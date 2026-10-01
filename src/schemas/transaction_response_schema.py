from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.enum.transaction_type import TransactionType


class TransactionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    transaction_type: TransactionType
    amount: float
    created_at: datetime
