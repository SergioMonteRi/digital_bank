from uuid import UUID

from pydantic import BaseModel

from src.enum.client_type import ClientType
from src.enum.transaction_type import TransactionType


class CreateTransactionSchema(BaseModel):
    client_id: UUID
    client_type: ClientType
    transaction_type: TransactionType
    amount: float
