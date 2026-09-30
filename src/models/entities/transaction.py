from datetime import datetime, timezone
from uuid import UUID, uuid7

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.custom_types.uuid import UUIDType
from src.database.base import Base
from src.enum.client_type import ClientType
from src.enum.transaction_type import TransactionType


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TransactionTable(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(UUIDType(), primary_key=True, default=uuid7)

    client_id: Mapped[UUID] = mapped_column(UUIDType(), nullable=False)

    client_type: Mapped[ClientType] = mapped_column(Enum(ClientType), nullable=False)

    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType), nullable=False
    )

    amount: Mapped[float] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=utc_now, nullable=False)
