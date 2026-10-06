from decimal import Decimal
from uuid import UUID, uuid7

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.custom_types.uuid import UUIDType
from src.database.base import Base


class IndividualTable(Base):
    __tablename__ = "individual"

    id: Mapped[UUID] = mapped_column(UUIDType(), primary_key=True, default=uuid7)

    monthly_income: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    age: Mapped[int]

    full_name: Mapped[str]

    phone: Mapped[str]

    email: Mapped[str]

    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2))
