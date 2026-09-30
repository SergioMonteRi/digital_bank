from uuid import UUID, uuid7

from sqlalchemy.orm import Mapped, mapped_column

from src.custom_types.uuid import UUIDType
from src.database.base import Base


class CompanyTable(Base):
    __tablename__ = "company"

    id: Mapped[UUID] = mapped_column(UUIDType(), primary_key=True, default=uuid7)

    monthly_revenue: Mapped[float]

    company_name: Mapped[str]

    phone: Mapped[str]

    email: Mapped[str]

    category: Mapped[str]

    balance: Mapped[float]
