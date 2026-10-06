from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from src.enum.client_type import ClientType
from src.enum.transaction_type import TransactionType


class CreateTransactionSchema(BaseModel):
    client_id: UUID
    client_type: ClientType
    transaction_type: TransactionType
    amount: Decimal = Field(max_digits=12, decimal_places=2)
