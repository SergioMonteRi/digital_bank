from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class CompanyTable(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    monthly_revenue: Mapped[float]
    company_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    category: Mapped[str]
    balance: Mapped[float]
